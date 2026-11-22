import flet as ft
from supabase import create_client, Client

SUPABASE_URL = "https://lcohplmtpqbtszgwkhdh.supabase.co"
SUPABASE_KEY = "sb_publishable_fw0BVn8o1G0yeR187f-gCA_1rkUGBC1"

def main(page: ft.Page):
    page.title = "Flet + Supabase Test"
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    status_text = ft.Text("Нажмите кнопку для записи в БД")
    
    def add_visit(e):
        try:
            response = supabase.table("visits").insert({"note": "Test from Flet App"}).execute()
            status_text.value = f"Успех! Записано: {len(response.data)}"
        except Exception as ex:
            status_text.value = f"Ошибка: {ex}"
        page.update()

    btn = ft.ElevatedButton("Записать в Supabase", on_click=add_visit)
    page.add(btn, status_text)

ft.app(target=main)