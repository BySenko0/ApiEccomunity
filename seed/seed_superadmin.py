from app.models.usuario import Usuario
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.usuario import hash_password

async def seed_superadmin(session: AsyncSession):
    email_superadmin = "super@admin.com"
    password_superadmin = "superadmin123"

    result = await session.execute(select(Usuario).where(Usuario.Correo == email_superadmin))
    superadmin = result.scalar_one_or_none()

    if not superadmin:
        nuevo_admin = Usuario(
            Nombre = "SUPERADMIN",
            Correo = email_superadmin,
            Ubicacion = "Querétaro, México",
            contrasena = hash_password(password_superadmin),
            Rol = "super_admin",
            Estado = "Activo",
            Cooldown = "0",
            url_perfil = "",
            Imagen_perfil = "",
            Imagen_fondo = ""
        )
        session.add(nuevo_admin)
        await session.commit()
        print("🛡️ Superadmin creado.")
    else:
        print("🛡️ Superadmin ya existe.")