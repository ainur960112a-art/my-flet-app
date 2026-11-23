import flet as ft
from supabase import create_client, Client

SUPABASE_URL = "https://lcohplmtpqbtszgwkhdh.supabase.co"
SUPABASE_KEY = "sb_publishable_fw0BVn8o1G0yeR187f-gCA_1rkUGBC1" 
def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    new_item_input = ft.TextField(
        hint_text="Что купить?", 
        expand=True,
        on_submit=lambda e: add_item(e)
    )
    
    items_list = ft.Column(spacing=10)

    def load_items():
        items_list.controls.clear()
        try:
            response = supabase.table("shopping_list").select("*").order("id", desc=False).execute()
            
            for item in response.data:
                def create_toggle_handler(item_id, checkbox):
                    def toggle(e):
                        try:
                            supabase.table("shopping_list").update({"is_done": checkbox.value}).eq("id", item_id).execute()
                            load_items()
                        except Exception as ex:
                            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                            page.snack_bar.open = True
                            page.update()
                    return toggle

                checkbox = ft.Checkbox(
                    value=item["is_done"],
                    label=item["name"],
                    expand=True
                )
                checkbox.on_change = create_toggle_handler(item["id"], checkbox)
                items_list.controls.append(checkbox)
            
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка загрузки: {ex}"))
            page.snack_bar.open = True
            page.update()

    def add_item(e):
        if not new_item_input.value:
            return
        try:
            supabase.table("shopping_list").insert({"name": new_item_input.value}).execute()
            new_item_input.value = ""
            load_items()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка добавления: {ex}"))
            page.snack_bar.open = True
            page.update()

    add_button = ft.IconButton(
        icon=ft.icons.ADD_CIRCLE,
        icon_size=40,
        icon_color=ft.colors.GREEN,
        on_click=add_item
    )

    page.add(
        ft.Text("Мой список покупок", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([new_item_input, add_button]),
        ft.Divider(),
        items_list
    )

    load_items()

ft.run(main)

