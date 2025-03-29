import discord
import random
import os
import requests
from discord.ext import commands
from settings import settings
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def saludo(ctx,name):
    await ctx.send(f"Hola {name} bienvenido")

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(f"La suma de {left} con {right} es {left + right}")
@bot.command()
async def subtract(ctx, left: int, right: int):
    """Subtracts two numbers together."""
    await ctx.send(f"La resta de {left} con {right} es {left - right}")

@bot.command()
async def programacion(ctx):
    programacion = os.listdir('programacion')
    with open(f'programacion/{random.choice(programacion)}', 'rb') as f:
            picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)
@bot.command()
async def memes(ctx):
    memes = os.listdir('memes')
    with open(f'memes/{random.choice(memes)}', 'rb') as f:
            picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Una vez que llamamos al comando duck, 
    el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command()
async def poke(ctx,arg):
    try:
        pokemon = arg.split(" ",1)[0].lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokemon)
        if result.text == "Not Found":
            await ctx.send("Pokemon no encontrado")
        else:
            image_url = result.json()["sprites"]["front_default"]
            print(image_url)
            await ctx.send(image_url)

    except Exception as e:
        print("Error:", e)
@poke.error
async def error_type(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send("Tienes que darme un pokemon")

@bot.command()
async def limpiar(ctx):
    await ctx.channel.purge()
    await ctx.send("Mensajes eliminados", delete_after = 3)

@bot.command()
async def formulas(ctx):
    await ctx.send(f"""
    Hola, soy un bot {bot.user}!
    """)# esta linea saluda
    await ctx.send("Quieres hablar de la contaminación? responde si o no x=")
    # Esperar la respuesta del usuario
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response = await bot.wait_for('message', check=check)
    if response:
        if response.content == 'si':
            await ctx.send("""
                    La contaminación es un problema que afecta a todo el planeta Tierra, existen diferentes tipos
                    pero todas tienen algo en comun, las basuras o residuos desechados se quedan en un mismo lugar
                    por mucho tiempo
                            """)   
        else:
            await ctx.send("Está bien, si alguna vez necesitas saber sobre otros juegos, estaremos en contacto.")
    else:
        await ctx.send("Lo siento, no pude entender tu respuesta. Inténtalo de nuevo.")
 
    await ctx.send("Quieres saber qué tipos de contaminacion existen?, responde 'si' o 'no'.")
    def check1(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content in ['si', 'no']
    response1 = await bot.wait_for('message', check=check1)
    if response1:
        if response1.content == "si":
            await ctx.send("""
                        1. La contaminación de residuos solidos.
                        2. La contaminacion del aire.
                            """) 
        else:
            await ctx.send("Está bien, si alguna vez necesitas hablar sobre juegos, estaremos en contacto.")
    else:
        await ctx.send("Lo siento, no pude entender tu respuesta. Inténtalo de nuevo.")

@bot.command()
async def mostrar(ctx):
    """Lista los nombres de los archivos en la carpeta 'imagenes'."""
    imagenes = os.listdir('__pycache__\Formulas')
    if imagenes:
        await ctx.send("Las imágenes disponibles son:\n" + "\n".join(imagenes))
    else:
        await ctx.send("No hay imágenes disponibles en la carpeta 'imagenes'.")
@bot.command()
async def enviar(ctx, nombre_imagen: str):
    """Envía la imagen especificada por el usuario."""
    imagenes = os.listdir('__pycache__\Formulas')
    if nombre_imagen in imagenes:
        with open(f'__pycache__\Formulas/{nombre_imagen}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(file=picture)
    else:
        await ctx.send(f"No se encontró la imagen '{nombre_imagen}'. Asegúrate de que el nombre sea correcto.")

bot.run(settings["TOKEN"])
