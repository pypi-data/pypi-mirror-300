from nautobot.core.apps import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuImportButton, NavMenuTab
# TODO: this menu_item does not work

menu_items = (
    NavMenuTab(
        name="Example Menu",
        weight=151,
        groups=(
            NavMenuGroup(
                name="Example Group 1",
                weight=100,
                items=(
                    NavMenuItem(
                        link="plugins:py_populate_dcim:home",
                        name="Etherflow's DCIM Populator",
                        # permissions=[
                        #     "example_app.view_examplemodel"
                        # ],
                        buttons=(
                            NavMenuAddButton(
                                link="plugins:py_populate_dcim:home",
                            ),
                            # NavMenuImportButton(
                            #     link="plugins:example_app:examplemodel_import",
                            #     permissions=[
                            #         "example_app.add_examplemodel"
                            #     ],
                            # ),
                        ),
                    ),
                ),
            ),
        ),
    ),
)
