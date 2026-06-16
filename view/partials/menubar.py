from PyQt6.QtWidgets import QMenuBar


class MenuBar(QMenuBar):
    def __init__(self, actions, parent=None):
        super().__init__(parent)
        self.app_actions = actions

        menu_specs = [
            ("&Experimente", [
                self.app_actions.experiment_new,
                self.app_actions.experiment_load,
                self.app_actions.experiment_save,
                self.app_actions.experiment_delete,
            ]),
            ("&Messreihen", [
                self.app_actions.measurement_new,
                self.app_actions.measurement_import,
                self.app_actions.measurement_save,
                self.app_actions.measurement_delete,
            ]),
            ("&Plots", [self.app_actions.plot_export]),
        ]

        for title, action_list in menu_specs:
            menu = self.addMenu(title)
            for action in action_list:
                menu.addAction(action)