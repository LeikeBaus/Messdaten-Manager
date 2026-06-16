from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QToolBar, QStyle


class ToolBar(QToolBar):
    def __init__(self, actions, parent=None):
        super().__init__(parent)
        self.app_actions = actions

        self.setIconSize(QSize(20, 20))
        self.setMovable(False)

        icon_specs = [
            (self.app_actions.experiment_new, QStyle.StandardPixmap.SP_FileDialogNewFolder),
            (self.app_actions.experiment_load, QStyle.StandardPixmap.SP_DialogOpenButton),
            (self.app_actions.experiment_save, QStyle.StandardPixmap.SP_DialogSaveButton),
            (self.app_actions.experiment_delete, QStyle.StandardPixmap.SP_TrashIcon),
            (self.app_actions.measurement_new, QStyle.StandardPixmap.SP_FileIcon),
            (self.app_actions.measurement_import, QStyle.StandardPixmap.SP_ArrowDown),
            (self.app_actions.measurement_save, QStyle.StandardPixmap.SP_DialogSaveButton),
            (self.app_actions.measurement_delete, QStyle.StandardPixmap.SP_TrashIcon),
            (self.app_actions.plot_export, QStyle.StandardPixmap.SP_DialogSaveButton),
        ]

        for action, icon in icon_specs:
            action.setIcon(self.style().standardIcon(icon))

        action_groups = [
            [
                self.app_actions.experiment_new,
                self.app_actions.experiment_load,
                self.app_actions.experiment_save,
                self.app_actions.experiment_delete,
            ],
            [
                self.app_actions.measurement_new,
                self.app_actions.measurement_import,
                self.app_actions.measurement_save,
                self.app_actions.measurement_delete,
            ],
            [self.app_actions.plot_export],
        ]

        for index, action_group in enumerate(action_groups):
            for action in action_group:
                self.addAction(action)
            if index < len(action_groups) - 1:
                self.addSeparator()