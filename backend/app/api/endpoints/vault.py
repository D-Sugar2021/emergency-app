import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.core.encryption import decrypt


router = APIRouter()


@router.get("/", response_model=schemas.GuardianVault)
async def read_vault(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the current user's Guardian Vault.
    """
    vault = await crud.crud_guardian_vault.get(db, user_id=current_user.id)
    if not vault:
        raise HTTPException(status_code=404, detail="Vault not found")
    return vault


@router.put("/", response_model=schemas.GuardianVault)
async def update_vault(
    *,
    db: AsyncSession = Depends(deps.get_db),
    vault_in: schemas.GuardianVaultCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or update the current user's Guardian Vault.
    """
    vault_db_obj = await crud.crud_guardian_vault.create_or_update(
        db, obj_in=vault_in, user_id=current_user.id
    )
    decrypted_data = decrypt(vault_db_obj.encrypted_data)
    return json.loads(decrypted_data)
