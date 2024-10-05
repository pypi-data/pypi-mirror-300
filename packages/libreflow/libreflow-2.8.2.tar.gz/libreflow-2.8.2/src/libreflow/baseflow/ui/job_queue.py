import os
import subprocess
import pprint
import six
import time
import timeago
from datetime import datetime, timedelta
from minio import Minio
# from ..scripts.minio_progress import Progress

from kabaret import flow
from kabaret.app.ui.gui.widgets.flow.flow_view import QtWidgets, QtCore, QtGui, CustomPageWidget
from kabaret.app.ui.gui.widgets.flow.flow_field import ObjectActionMenuManager
from kabaret.app import resources
from kabaret.app.ui.gui.icons import flow as _

from .controller import Controller

class RunnerSignals(QtCore.QObject):
    
    # Signals for QRunnable must be outside the class.

    progress = QtCore.Signal(dict)
    progress_refresh = QtCore.Signal(dict, object)
    finished = QtCore.Signal()


class RefreshRunner(QtCore.QRunnable):

    # Main worker for update Job list widget

    def __init__(self, page_widget, oid, item=None):
        super(RefreshRunner, self).__init__()
        self.page_widget = page_widget
        self.signals = RunnerSignals()
        self.oid = oid
        self.item = item

    def run(self):
        emitter_oid = self.page_widget.session.cmds.Flow.call(
            self.oid, 'get_property', ['emitter_oid'], {}
        )
        split = emitter_oid.split('/')
        indices = list(range(len(split) - 4, 2, -2))
        indices[:0] = [len(split)-1]
        source_display = ' – '.join([split[i] for i in reversed(indices)])

        job_type   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['type'], {}) 
        status = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['status'], {})
        size = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['file_size'], {})
        user   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['requested_by_user'], {})
        site   = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['requested_by_studio'], {})

        date = self.page_widget.session.cmds.Flow.call( self.oid, 'get_property', ['date'], {})

        data = {
            "oid": self.oid,
            "emitter_oid": emitter_oid,
            "source_display": source_display,
            "job_type": job_type,
            "size": size,
            "status": status,
            "user": user,
            "site": site,
            "date": date
        }

        if self.item:
            self.signals.progress_refresh.emit(data, self.item)
        else:
            self.signals.progress.emit(data)

        self.signals.finished.emit()


def get_icon_ref(icon_name, resource_folder='icons.flow'):
    if isinstance(icon_name, six.string_types):
        icon_ref = (resource_folder, icon_name)
    else:
        icon_ref = icon_name

    return icon_ref

class JobQueueFooter(QtWidgets.QWidget):
    def __init__(self, page_widget):
        super(JobQueueFooter,self).__init__(page_widget)
        self.page_widget = page_widget
        self.build()

    def build(self):
        self.stats_label = QtWidgets.QLabel()
        self.loading_label = QtWidgets.QLabel()
        self.last_auto_sync_label = QtWidgets.QLabel()
        self.last_manual_sync_label = QtWidgets.QLabel()

        self.stats_label.hide()
        self.last_auto_sync_label.hide()
        self.last_manual_sync_label.hide()

        self.loading_label.setText('Loading queue...')


        flo = QtWidgets.QGridLayout()
        flo.addWidget(self.stats_label,0,0)
        flo.addWidget(self.loading_label,1,0)
        flo.addWidget(self.last_auto_sync_label,0,1, alignment=QtCore.Qt.AlignRight)
        flo.addWidget(self.last_manual_sync_label,1,1, alignment=QtCore.Qt.AlignRight)

        self.setLayout(flo)

    def refresh(self):

        site_oid = os.path.split(self.page_widget.oid)[0]

        all_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [], {})
        all_count = f'{all_count} Jobs in queue'
        processed_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "PROCESSED"], {})
        processed_count = f'<font color="#61f791">{processed_count} PROCESSED</font>'
        error_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "ERROR"], {})
        error_count = f'<font color="#ff5842">{error_count} ERROR</font>'
        waiting_count = self.page_widget.session.cmds.Flow.call( site_oid, 'count_jobs', [None, "WAITING"], {})
        waiting_count = f'<font color="#EFDD5B">{waiting_count} WAITING</font>'

        last_auto_sync = self.page_widget.session.cmds.Flow.get_value(self.page_widget.oid + '/last_auto_sync')
        if last_auto_sync is not None :
            date = datetime.fromtimestamp(last_auto_sync)
            full_date = date.strftime('%Y-%m-%d %H:%M:%S')
            nice_date = timeago.format(full_date, datetime.now())
            self.last_auto_sync_label.setText(f'Last auto sync: {full_date} ({nice_date})')


        last_manual_sync = self.page_widget.session.cmds.Flow.get_value(self.page_widget.oid + '/last_manual_sync')
        if last_manual_sync is not None :
            date = datetime.fromtimestamp(last_manual_sync)
            full_date = date.strftime('%Y-%m-%d %H:%M:%S')
            nice_date = timeago.format(full_date, datetime.now())
            self.last_manual_sync_label.setText(f'Last manual sync: {full_date} ({nice_date})')
        
        self.stats_label.setText(f'{all_count} / {processed_count} - {waiting_count} - {error_count}')
    
    # def get_summary(self):
    #     text = self.page_widget.session.cmds.Flow.call(
    #                 self.page_widget.oid, 'summary', [], {})
    #     return text

class JobQueueHeader(QtWidgets.QWidget):

    def __init__(self, content_widget):
        super(JobQueueHeader,self).__init__(content_widget)
        self.content_widget = content_widget
        self.page_widget = self.content_widget.page_widget
        self.build()

    def build(self):
        self.filter_status_label = QtWidgets.QLabel('Filter status')

        self.filter_status_combobox = QtWidgets.QComboBox()
        self.filter_status_combobox.addItems(['ALL', 'PROCESSED', 'WAITING', 'ERROR'])
        self.filter_status_combobox.setCurrentIndex(0)
        self.filter_status_combobox.currentTextChanged.connect(self._on_filter_status_changed)
        self.filter_status_combobox.setView(QtWidgets.QListView())
        self.filter_status_combobox.setStyleSheet('''
        QComboBox {
            background-color: #232d33;
            border: 2px solid #4c4c4c;
            border-radius: 7px;
        }
        QComboBox::drop-down {
            background-color: #616160;
            border-radius: 4px;
        }
        QComboBox QAbstractItemView::item {
            min-height: 20px;
        }'''
        )
        self.auto_refresh_box = QtWidgets.QCheckBox('Enable Auto-refresh')
        self.auto_refresh_box.setChecked(True)
        self.auto_refresh_box.stateChanged.connect(self._on_auto_refresh_toggle)

        self.clear_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'clean'))), '')
        self.clear_button.clicked.connect(self._on_clear_button_clicked)
        self.clear_button.setIconSize(QtCore.QSize(20,20))
        self.clear_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.clear_button.setToolTip("Clear queue")

        self.removejobs_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'waiting'))), '')
        self.removejobs_button.clicked.connect(self._on_removejobs_button_clicked)
        self.removejobs_button.setIconSize(QtCore.QSize(20,20))
        self.removejobs_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.removejobs_button.setToolTip("Remove outdated jobs")

        self.resetjobs_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'refresh'))), '')
        self.resetjobs_button.clicked.connect(self._on_resetjobs_button_clicked)
        self.resetjobs_button.setIconSize(QtCore.QSize(20,20))
        self.resetjobs_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.resetjobs_button.setToolTip("Reset erroneous jobs")

        # self.test_button = QtWidgets.QPushButton(QtGui.QIcon(resources.get_icon(('icons.libreflow', 'refresh'))), '')
        # self.test_button.clicked.connect(self._on_test_button_clicked)
        # self.test_button.setIconSize(QtCore.QSize(20,20))
        # self.test_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        hlo = QtWidgets.QHBoxLayout()
        hlo.addWidget(self.filter_status_label)
        hlo.addWidget(self.filter_status_combobox)
        hlo.addWidget(self.auto_refresh_box)
        hlo.addStretch()
        hlo.addWidget(self.clear_button)
        hlo.addWidget(self.resetjobs_button)
        hlo.addWidget(self.removejobs_button)
        # hlo.addWidget(self.test_button)

        self.setLayout(hlo)
    
    def _on_clear_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/clear_queue"
            )

    def _on_removejobs_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/remove_outdated_jobs"
            )
        self.page_widget.refresh_timer.stop()
        self.page_widget.refresh_list()

    def _on_resetjobs_button_clicked(self):
        self.page_widget.page.show_action_dialog(
                f"{self.page_widget.oid}/job_list/reset_jobs"
            )
        self.page_widget.refresh_timer.stop()
        self.page_widget.refresh_list()
    
    def _on_auto_refresh_toggle(self,value):
        if self.auto_refresh_box.isChecked() is True :
            self.page_widget.refresh_timer.start()
        else : self.page_widget.refresh_timer.stop()
    
    def _on_filter_status_changed(self, value):
        self.content_widget.listbox.list.refresh_filter(value)


class JobData(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree, data):
        super(JobData,self).__init__(tree)
        self.tree = tree
        self.page_widget = tree.page_widget
        self.job_data = data
        self.refresh()
    
    def refresh(self):
        if self.job_data['job_type'] == "Download" :
            self.setIcon(0,self.tree.dl_icon)
        else : self.setIcon(0,self.tree.up_icon)

        self.setText(0, self.job_data['source_display'])
        

        if self.job_data['status'] == "PROCESSED":
            for i in range(self.tree.columnCount()):
                self.setForeground(i,QtGui.QBrush(QtGui.QColor(150, 150, 150)))

        locale = QtCore.QLocale()
        if self.job_data["size"] != '' :
            display_size = locale.formattedDataSize(self.job_data["size"],format = locale.DataSizeTraditionalFormat)
        else : display_size = ''
        self.setText(1, display_size)

        self.setText(2, self.job_data['status'])
    
        self.setData(3, QtCore.Qt.DisplayRole, QtCore.QDateTime.fromSecsSinceEpoch(int(self.job_data['date'])))
        self.setText(4, self.job_data['user'])
        self.setText(5, self.job_data['site'])

        self.setToolTip(0,self.job_data['source_display'])

        self.tree.refresh_completed()

class JobQueueListWidget(QtWidgets.QTreeWidget):
    def __init__(self,box_widget):
        super(JobQueueListWidget, self).__init__(box_widget)
        self.box_widget = box_widget
        self.content_widget = self.box_widget.content_widget
        self.page_widget = self.content_widget.page_widget

        self.setStyleSheet('''QTreeWidget {
                                background-color: transparent;
                                border: none;
                            }
                            QTreeWidget::item {
                                padding: 4px;
                            } 
                            QHeaderView {
                                background-color: transparent;
                                border-top: none;
                                border-left: none;
                                border-right: none;
                                border-color: #535151
                            }
                            QHeaderView::section {
                                background-color: transparent; 
                                border-color: #535151
                            }'''
                            )

        self.setHeaderLabels(['Name', 'Size', 'Status', 'Emitted On', 'User', 'Site'])

        self.dl_icon = QtGui.QIcon(resources.get_icon(('icons.libreflow', 'download')))
        self.up_icon = QtGui.QIcon(resources.get_icon(('icons.libreflow', 'upload')))
        
        self.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        # self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.setTextElideMode(QtCore.Qt.ElideLeft)
        self.setSortingEnabled(True)
        self.sortByColumn(3, QtCore.Qt.DescendingOrder)
        self.setRootIsDecorated(False)

        self.action_manager = ObjectActionMenuManager(
            self.page_widget.session, self.page_widget.page.show_action_dialog, 'Flow.map'
        )

        self.itemDoubleClicked.connect(self.on_item_doubleClicked)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu_requested)

        self.refresh()

    def refresh(self):
        self.blockSignals(True)
        self.page_widget.data_fetched = False
        
        self.page_widget.start = time.time()

        map_oid = self.page_widget.oid + "/job_list"
        self.oid_list = self.page_widget.session.cmds.Flow.get_mapped_oids(map_oid)

        self.page_widget.footer.refresh()

        # if force_update:
        #     self.clear()
        #     self.page_widget.force_update = True
        #     self.page_widget.content.popup.show()
        # elif self.page_widget.get_cache_key() is None:
        #     self.page_widget.force_update = True
        
        self.blockSignals(False)

    def refresh_completed(self):
        if self.topLevelItemCount() == self.page_widget.jobs_count and self.page_widget.data_fetched is False:
            print('Job queue built in %.3fs' % (time.time() - self.page_widget.start))
            self.page_widget.clearPool()
            self.page_widget.refresh_timer.start()
            if self.content_widget.header.auto_refresh_box.isChecked() is True:
               self.page_widget.refresh_timer.start()
            self.page_widget.footer.loading_label.hide() 
            self.page_widget.footer.stats_label.show()
            self.page_widget.footer.last_auto_sync_label.show()
            self.page_widget.footer.last_manual_sync_label.show()
            self.page_widget.data_fetched = True
            return True

    def addJob(self, data):
        self.blockSignals(True)

        item = JobData(self, data)

        self.setColumnWidth(0, 400)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)
        self.resizeColumnToContents(3)
        self.resizeColumnToContents(4)
        self.resizeColumnToContents(5)
        self.resizeColumnToContents(6)

        self.blockSignals(False)

    def jobExists(self, oid):
        job_items = [self.topLevelItem(i) for i in range(self.topLevelItemCount()) if self.topLevelItem(i).job_data['oid'] == oid]
        return job_items[0] if job_items else None
    
    def refresh_filter(self, value):
        self.reset_filter()
        if value == 'ALL':
            return
        
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).job_data['status'] != value:
                self.topLevelItem(i).setHidden(True)
    
    def reset_filter(self):
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).setHidden(False)
    
    def on_item_doubleClicked(self,item):
        self.page_widget.page.goto(item.job_data['oid'])
    
    def _on_context_menu_requested(self, pos):

        action_menu = QtWidgets.QMenu(self)

        index = self.indexAt(pos)

        if not index.isValid():
            return

        item = self.itemAt(pos)

        has_actions = self.action_manager.update_oid_menu(
            item.job_data['oid'], action_menu, with_submenus=True
        )

        if has_actions:
            action_menu.exec_(self.viewport().mapToGlobal(pos))

    # def _on_action_menu_triggered(self, action_oid):
    #     self.page_widget.page.show_action_dialog(action_oid)


class JobQueueListBox(QtWidgets.QWidget):
    def __init__(self, content_widget):
        super(JobQueueListBox, self).__init__(content_widget)
        self.setObjectName('JobQueueListBox')
        self.content_widget = content_widget
        self.page_widget = self.content_widget.page_widget

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('#JobQueueListBox { background-color: #626261; border-radius: 5px; }')

        self.build()

    def build(self):
        box = QtWidgets.QVBoxLayout(self)
        self.list = JobQueueListWidget(self)
        box.addWidget(self.list)

class JobQueueContent(QtWidgets.QWidget):
    def __init__(self, page_widget):
        super(JobQueueContent, self).__init__(page_widget)
        self.setObjectName('JobQueueContent')
        self.page_widget = page_widget

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('#JobQueueContent { background-color: #232d33; border-radius: 5px; }')

        self.build()

    def build(self):
        grid = QtWidgets.QGridLayout(self)

        self.header = JobQueueHeader(self)
        self.listbox = JobQueueListBox(self)
        grid.addWidget(self.header, 0, 0)
        grid.addWidget(self.listbox, 1, 0)

class JobQueueWidget(CustomPageWidget):

    def build(self):
        self.__pool = QtCore.QThreadPool()
        self.__pool.setMaxThreadCount(self.__pool.globalInstance().maxThreadCount())

        self.data_fetched = False

        self.start = time.time()

        self.thread = QtCore.QThread()
        self.thread.started.connect(self.init_list)
        self.thread.finished.connect(self.thread.quit)

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.setInterval(5000)
        self.refresh_timer.timeout.connect(self.refresh_list)

        self.setStyleSheet('outline: 0;')

        self.footer = JobQueueFooter(self)
        self.content = JobQueueContent(self)

        vlo = QtWidgets.QVBoxLayout(self)
        vlo.setContentsMargins(0,0,0,0)
        vlo.setSpacing(1)
        vlo.addWidget(self.content)
        vlo.addWidget(self.footer)

        self.content.listbox.list.refresh()
        self.thread.start()
    
    def on_touch_event(self,oid):
        return None
    #     job_list_oid = self.oid + "/job_list"
    #     if oid == job_list_oid:
    #         print ("MAP TOUCHED")

    def init_list(self):
        self.jobs_count = len(self.content.listbox.list.oid_list)

        self.footer.stats_label.hide()
        self.footer.last_auto_sync_label.hide()
        self.footer.last_manual_sync_label.hide()

        for oid in self.content.listbox.list.oid_list:
            refresh_runner = RefreshRunner(self, oid)
            refresh_runner.signals.progress.connect(self.addJobWidget)
            self.__pool.start(refresh_runner)

        self.thread.finished.emit()
    
    def refresh_list(self):
        self.content.listbox.list.refresh()

        self.jobs_count = len(self.content.listbox.list.oid_list)
        self.footer.loading_label.show() 
        for oid in self.content.listbox.list.oid_list:
            # Check if already exists
            item = self.content.listbox.list.jobExists(oid)
            refresh_runner = RefreshRunner(self, oid, item)
            if item:
                refresh_runner.signals.progress_refresh.connect(self.updateJobWidget)
            else:
                print('ADD ITEM', oid)
                refresh_runner.signals.progress.connect(self.addJobWidget)

            self.__pool.start(refresh_runner)

        self.thread.finished.emit()

    def addJobWidget(self, data):
        self.content.listbox.list.addJob(data)
    
    def updateJobWidget(self, data, item):
        item.job_data = data
        item.refresh()
    
    def clearPool(self):
        self.__pool.clear()
    
    def refresh_test(self):
        print('REFRESH')
