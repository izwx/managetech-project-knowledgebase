from django.contrib import admin
from .models import TrelloConfiguration, TrelloBoard, TrelloUser, TrelloList, TrelloCard, TrelloAction, MyTrelloBoard

# Register your models here.

@admin.register(TrelloBoard)
class TrelloBoardAdmin(admin.ModelAdmin):
    list_display=('boardId', 'name', 'boardUrl')

@admin.register(TrelloUser)
class TrelloUserAdmin(admin.ModelAdmin):
    list_display=('userId', 'username', 'userUrl', 'email')

@admin.register(TrelloList)
class TrelloListAdmin(admin.ModelAdmin):
    list_display=('listId', 'name', 'board', )

@admin.register(TrelloCard)
class TrelloCardAdmin(admin.ModelAdmin):
    list_display=('cardId', 'name', 'board', 'list',)

@admin.register(TrelloAction)
class TrelloActionAdmin(admin.ModelAdmin):
    pass