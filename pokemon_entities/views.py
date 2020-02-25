import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    entities = PokemonEntity.objects.all()
    for entity in entities:
        pokemon = entity.pokemon
        pokemon_image_url = request.build_absolute_uri(pokemon.img_url.url)
        add_pokemon(
            folium_map, entity.lat, entity.lon, pokemon.title_ru, pokemon_image_url)

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.img_url.url,
            'title_ru': pokemon.title_ru,
        })
    
    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon_id = int(pokemon_id)
    try:
        requested_pokemon = Pokemon.objects.get(id=requested_pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    previous_evolution = None
    next_evolution = None
    
    if requested_pokemon.previous_evolution:
        pokemon_previous_evolution = requested_pokemon.previous_evolution
        previous_evolution = {
                'pokemon_id': pokemon_previous_evolution.id,
                'title_ru': pokemon_previous_evolution.title_ru,
                'img_url': request.build_absolute_uri(pokemon_previous_evolution.img_url.url)
                }
    pokemon_next_evolution = requested_pokemon.next_evolutions.first()
    if pokemon_next_evolution:
        next_evolution = {
                'pokemon_id': pokemon_next_evolution.id,
                'title_ru': pokemon_next_evolution.title_ru,
                'img_url': request.build_absolute_uri(pokemon_next_evolution.img_url.url)
                }
    
    entities = requested_pokemon.pokemon_entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in entities:
        pokemon_image_url = request.build_absolute_uri(requested_pokemon.img_url.url)
        add_pokemon(
            folium_map, entity.lat, entity.lon,
            requested_pokemon.title_ru, pokemon_image_url)

    pokemon = {
            'pokemon_id': requested_pokemon_id,
            'title_ru': requested_pokemon.title_ru,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
            'description': requested_pokemon.description,
            'img_url': pokemon_image_url,
            'previous_evolution': previous_evolution,
            'next_evolution': next_evolution
            }
    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
