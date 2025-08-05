from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.publicacion import Publicacion
from app.schemas.publicacion import PublicacionCreate, PublicacionUpdate
from app.models.usuario import Usuario
from app.models.likes_publicaciones import Likes_Publicaciones
import os

async def get_all(db: AsyncSession):
    query = (
        select( 
            Publicacion.Id,
            Publicacion.Titulo,
            Publicacion.Contenido,
            Publicacion.Imagen,
            Publicacion.FechaPublicacion,
            Publicacion.id_Usuario,
            Usuario.Nombre.label("NombreUsuario"),
            Usuario.Imagen_perfil.label("ImagenPerfilUsuario"),
        )
        .join(Usuario, Publicacion.id_Usuario == Usuario.Id)
        .order_by(Publicacion.FechaPublicacion.desc())
    )
    result = await db.execute(query)
    publicaciones = result.mappings().all()
    
    publicaciones_con_url = []
    for pub in publicaciones:
        pub_dict = dict(pub)


        APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
        STATIC_IMG_FILES_PATH = os.getenv("STATIC_IMG_FILES_PATH", "/static/imagenes")
        
        if pub_dict['Imagen']:
            pub_dict['ImagenUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/publicaciones/{pub_dict['Imagen']}"
        else:
            pub_dict['ImagenUrl'] = None
        if pub_dict['ImagenPerfilUsuario']:
            pub_dict['ImagenPerfilUsuarioUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/perfil/{pub_dict['ImagenPerfilUsuario']}"
        else:
            pub_dict['ImagenPerfilUsuarioUrl'] = None

        publicaciones_con_url.append(pub_dict)
    
    return publicaciones_con_url

async def get_by_id(db: AsyncSession, pub_id: int):
    query = (
        select(
            Publicacion.Id,
            Publicacion.Titulo,
            Publicacion.Contenido,
            Publicacion.Imagen,
            Publicacion.FechaPublicacion,
            Publicacion.id_Usuario,
            Usuario.Nombre.label("NombreUsuario"),
            Usuario.Imagen_perfil.label("ImagenPerfilUsuario"),
        )
        .join(Usuario, Publicacion.id_Usuario == Usuario.Id)
        .where(Publicacion.Id == pub_id)
    )
    result = await db.execute(query)
    publicacion = result.mappings().first()
    
    if publicacion:

        pub_dict = dict(publicacion)

        APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
        STATIC_IMG_FILES_PATH = os.getenv("STATIC_IMG_FILES_PATH", "/static/imagenes")

        if pub_dict['Imagen']:
            pub_dict['ImagenUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/publicaciones/{pub_dict['Imagen']}"
        else:
            pub_dict['ImagenUrl'] = None
        if pub_dict['ImagenPerfilUsuario']:
            pub_dict['ImagenPerfilUsuarioUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/perfil/{pub_dict['ImagenPerfilUsuario']}"
        else:
            pub_dict['ImagenPerfilUsuarioUrl'] = None
        return pub_dict
    
    return None

async def create(db: AsyncSession, data: PublicacionCreate):
    nueva = Publicacion(**data.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

async def update(db: AsyncSession, pub_id: int, data: PublicacionUpdate):
    result = await db.execute(select(Publicacion).where(Publicacion.Id == pub_id))
    pub = result.scalar_one_or_none()

    if not pub:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(pub, key, value)

    await db.commit()
    await db.refresh(pub)

    return pub


async def get_by_user_id(db: AsyncSession, user_id: int):
    query = (
        select(
            Publicacion.Id,
            Publicacion.Titulo,
            Publicacion.Contenido,
            Publicacion.Imagen,
            Publicacion.FechaPublicacion,
            Publicacion.id_Usuario,
            Usuario.Nombre.label("NombreUsuario"),
            Usuario.Imagen_perfil.label("ImagenPerfilUsuario"),
        )
        .join(Usuario, Publicacion.id_Usuario == Usuario.Id)
        .where(Publicacion.id_Usuario == user_id)
        .order_by(Publicacion.FechaPublicacion.desc())
    )
    result = await db.execute(query)
    publicaciones = result.mappings().all()
    
    publicaciones_con_url = []

    for pub in publicaciones:
        
        pub_dict = dict(pub)
        
        APP_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
        STATIC_IMG_FILES_PATH = os.getenv("STATIC_IMG_FILES_PATH", "/static/imagenes")

        if pub_dict['Imagen']:
            pub_dict['ImagenUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/publicaciones/{pub_dict['Imagen']}"
        else:
            pub_dict['ImagenUrl'] = None
        if pub_dict['ImagenPerfilUsuario']:
            pub_dict['ImagenPerfilUsuarioUrl'] = f"{APP_BASE_URL}{STATIC_IMG_FILES_PATH}/perfil/{pub_dict['ImagenPerfilUsuario']}"
        else:
            pub_dict['ImagenPerfilUsuarioUrl'] = None
        publicaciones_con_url.append(pub_dict)
    
    return publicaciones_con_url

async def delete(db: AsyncSession, pub_id: int):
    result = await db.execute(select(Publicacion).where(Publicacion.Id == pub_id))
    pub = result.scalar_one_or_none()

    if not pub:
        return None

    await db.delete(pub)
    await db.commit()
    return pub

async def get_tendencias(db: AsyncSession):
    query = (
        select(
            Publicacion.Titulo,
            Publicacion.FechaPublicacion,
            func.count(Likes_Publicaciones.Id).label("cuenta_likes")
        )
        .select_from(
            Publicacion
        )
        .join(Likes_Publicaciones, Likes_Publicaciones.id_Publicacion == Publicacion.Id)
        .group_by(Publicacion.Id)
        .order_by(func.count(Likes_Publicaciones.Id).desc())
        .limit(10)
    )
    result = await db.execute(query)
    tendencias = result.mappings().all()
    return tendencias

async def get_tendencias_usuarios(db: AsyncSession):
    query = (
        select(
            Usuario.Nombre.label("NombreUsuario"),
            func.count(Publicacion.Id).label("cuenta_publicaciones")
        )
        .select_from(
            Usuario
        )
        .join(Publicacion, Publicacion.id_Usuario == Usuario.Id)
        .group_by(Usuario.Id)
        .order_by(func.count(Publicacion.Id).desc())
        .limit(10)
    )
    result = await db.execute(query)
    tendencias = result.mappings().all()
    return tendencias