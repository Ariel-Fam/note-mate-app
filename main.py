# import flet as ft
#
# def main(page: ft.Page):
#     page.title = "Multi-Page Note App"
#     page.window_width = 900
#     page.window_height = 700
#     page.window_resizable = False
#     page.bgcolor = ft.colors.WHITE
#
#     # Pages storage
#     def route_change(e):
#         page.views.clear()
#
#         if page.route == "/":
#             page.views.append(description_view())
#         elif page.route == "/app":
#             page.views.append(note_app_view())
#
#         page.update()
#
#     # Back button logic
#     def view_pop(e):
#         page.views.pop()
#         page.update()
#
#     # Description View
#     def description_view():
#         return ft.View(
#             "/",
#             controls=[
#                 ft.Text("Welcome to NoteMate", size=30, weight=ft.FontWeight.BOLD),
#                 ft.Text(
#                     "NoteMate is your digital companion for capturing ideas, tasks, and inspirations effortlessly. "
#                     "With a minimalist design and intuitive interface, you can quickly jot down notes and stay organized. "
#                     "Perfect for students, professionals, or anyone who loves structured thought. "
#                     "Your data is locally stored for privacy, and the app launches instantly on your desktop for maximum productivity. "
#                     "Take notes, add timestamps, and enjoy a distraction-free writing experience.",
#                     size=16,
#                     width=700,
#                     selectable=True,
#                 ),
#                 ft.ElevatedButton("Launch App", on_click=lambda _: page.go("/app")),
#             ],
#             vertical_alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         )
#
#     # Main App View
#     def note_app_view():
#         notes = ft.TextField(label="Write your note...", multiline=True, min_lines=5, max_lines=10, expand=True)
#         output = ft.Column()
#
#         def save_note(e):
#             if notes.value:
#                 output.controls.append(ft.Text(f"📝 {notes.value.strip()}", size=14))
#                 notes.value = ""
#                 page.update()
#
#         return ft.View(
#             "/app",
#             controls=[
#                 ft.Row([
#                     ft.Text("🗒️ NoteMate", size=24, weight=ft.FontWeight.BOLD),
#                     ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go("/")),
#                 ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
#                 notes,
#                 ft.ElevatedButton("Save Note", on_click=save_note),
#                 ft.Divider(),
#                 ft.Text("Saved Notes:", size=18, weight=ft.FontWeight.BOLD),
#                 output
#             ],
#             scroll=ft.ScrollMode.ALWAYS,
#         )
#
#     page.on_route_change = route_change
#     page.on_view_pop = view_pop
#
#     page.go(page.route)
#
# # Run App
# ft.app(target=main)












import flet as ft

import sqlite3 as sq

def main(page: ft.Page):
    page.title = "Note Mate"
    page.window_width = 900
    page.window.height = 700
    page.window_resizable = False
    page.window.bgcolor = "blue"
    page.scroll = ft.ScrollMode.ALWAYS

    # Database Set up:

    conn = sq.connect("notes.db")
    cursor = conn.cursor()

    response_list = []

    history_list = []

    # Functions:

    def save_note(e):

        if notes_field.value:

            value = notes_field.value.strip()


            cursor.execute("INSERT INTO notes (note) VALUES (?)", (value,))
            conn.commit()

            cursor.execute("INSERT INTO history (note) VALUES (?)", (value,))
            conn.commit()

            output_column.controls.append(ft.Row(controls=[ft.Text(f"📝 {value}",
                                                                   size=17, color="white",), ft.Checkbox()], spacing=40))

            history_column.controls.append(ft.Row(controls=[ft.Text(f"📝 {value}",
                                                                   size=17, color="white", ), ft.Checkbox()],
                                                 spacing=40))

            output_column.offset = (0.05, 0)

            # for control in output_column.controls:
            #
            #     if control not in history_column:
            #         history_column.controls.append(control)

            history_column.offset = (0.05, 0)

            notes_field.value = ""
            page.update()

    def clear_notes(e):
        if output_column.controls:
            output_column.controls.clear()
            page.update()

        cursor.execute("DELETE FROM notes")
        conn.commit()

    def clear_history(e):

        if history_column.controls:

            history_column.controls.clear()

            page.update()

        cursor.execute("DELETE FROM history")
        conn.commit()





    # 1) Create your controls *once* at the top:
    notes_field = ft.TextField(
        label="Write your note...",
        multiline=True,
        min_lines=5,
        max_lines=10,
        expand=True,
        bgcolor="yellow",
        color="black"

    )
    output_column = ft.Column(alignment=ft.MainAxisAlignment.START)
    output_column.scroll = ft.ScrollMode.ALWAYS

    history_column = ft.Column()
    history_column.scroll = ft.ScrollMode.ALWAYS

    launch_logo = ft.Image("/images/launch_logo.png", width=200, height=140)

    launch_logo.offset = (1.4, 0)

    def render_from_db():

        cursor.execute("SELECT * FROM notes")

        rows = cursor.fetchall()

        for row in rows:
            response_list.append((row[0], row[1]))

        for item in response_list:
            output_column.controls.append(ft.Row(controls=[ft.Text(f"📝 {item[1]}",
                                                                   size=17, color="white", ), ft.Checkbox()],spacing=40))

        cursor.execute("SELECT * FROM history")

        rows2 = cursor.fetchall()

        for row in rows2:
            history_list.append((row[0], row[1]))

        for item in history_list:

            history_column.controls.append(ft.Row(controls=[ft.Text(f"📝 {item[1]}",
                                                                   size=17, color="white", ), ft.Checkbox()],spacing=40))

        page.update()

    render_from_db()

    def delete_note(e):
        if output_column.controls:
            output_column.controls.pop()
            page.update()

        cursor.execute("DELETE FROM notes WHERE id=(SELECT MAX(id) FROM notes)")
        conn.commit()



    # 2) Build each View once:
    description_view = ft.View(
        "/",
        controls=[

            ft.Image(src="/images/space_pointer.png", width=340, height=340),
            ft.Text("Welcome to NoteMate", size=30, weight=ft.FontWeight.BOLD),
            ft.Text(
                "NoteMate is your digital companion for capturing ideas, tasks, and inspirations effortlessly. "
                "With a minimalist design and intuitive interface, you can quickly jot down notes and stay organized. "
                "Perfect for students, professionals, or anyone who loves structured thought. "
                "Your data is locally stored for privacy, and the app launches instantly on your desktop for maximum productivity. "
                "Take notes, add timestamps, and enjoy a distraction-free writing experience.",
                size=16,
                width=700,
                selectable=True,
                color="black"
            ),
            ft.ElevatedButton("Launch App", on_click=lambda _: page.go("/app"), tooltip="Start writing notes"),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    description_view.scroll = ft.ScrollMode.ALWAYS
    description_view.bgcolor = ft.colors.BLUE_400

    note_app_view = ft.View(
        "/app",
        controls=[
            ft.Row(
                [
                    ft.Text("🗒️ NoteMate", size=24, weight=ft.FontWeight.BOLD,enable_interactive_selection=True,
                            selectable=True),
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"),
                                  tooltip="Back to description page"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            notes_field,
            ft.Row(controls=[
                ft.ElevatedButton("Save Note", on_click=save_note, tooltip="Save Note Bellow"),
                ft.ElevatedButton("Delete Note", on_click=delete_note, tooltip="Delete last Note"),
                ft.ElevatedButton("Clear Notes", on_click=clear_notes, tooltip="Delete all Notes"),
                ft.ElevatedButton("Notes History", icon=ft.Icons.HISTORY, on_click=lambda _: page.go("/history",),
                                  bgcolor="orange", color="black", icon_color="black", tooltip="View Notes History")
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text("Saved Notes:", size=18, weight=ft.FontWeight.BOLD),
            ft.Column(controls=[output_column, launch_logo], spacing=170)

        ],
        scroll=ft.ScrollMode.ALWAYS,
    )
    note_app_view.bgcolor = ft.colors.BLUE_900
    note_app_view.scroll = ft.ScrollMode.AUTO

    history_view = ft.View(route="/history", controls=[

        ft.Column(spacing=40, controls=[
            ft.Text("Notes History 📘", size=30),
            history_column,
            ft.ElevatedButton("Clear History", on_click=clear_history, bgcolor="yellow", color="Black",
                              tooltip="Clear History"),
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/app"), tooltip="Back to notes")
        ]),
    ])

    history_view.scroll = ft.ScrollMode.ALWAYS

    # 3) Route handler just swaps in the prebuilt views:
    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(description_view)
        if page.route == "/app":
            page.views.append(note_app_view)
        if page.route == "/history":
            page.views.append(history_view)

        page.update()

    def view_pop(e):
        page.views.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # 4) Kick things off:
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
