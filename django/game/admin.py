from django.contrib import admin
from .models import Board, Tile, Game, Player


class PlayerInline(admin.TabularInline):
    model = Player


class GameAdmin(admin.ModelAdmin):
    inlines = [
        PlayerInline,
    ]

admin.site.register(Board)
admin.site.register(Tile)
admin.site.register(Game, GameAdmin)
