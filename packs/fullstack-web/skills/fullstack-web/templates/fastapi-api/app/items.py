from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from .auth import get_current_user
from .db import get_session
from .models import Item, ItemCreate, ItemRead, ItemUpdate, User, utcnow

router = APIRouter(prefix="/items", tags=["items"])


def get_owned_item(item_id: int, user: User, session: Session) -> Item:
    item = session.get(Item, item_id)
    if not item or item.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.get("", response_model=list[ItemRead])
def list_items(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    q: str | None = Query(None, max_length=100),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[Item]:
    stmt = select(Item).where(Item.owner_id == user.id)
    if q:
        stmt = stmt.where(Item.title.contains(q))
    stmt = stmt.order_by(Item.created_at.desc()).offset((page - 1) * limit).limit(limit)
    return list(session.exec(stmt).all())


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> Item:
    item = Item(**data.model_dump(), owner_id=user.id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> Item:
    return get_owned_item(item_id, user, session)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int, data: ItemUpdate, user: User = Depends(get_current_user), session: Session = Depends(get_session)
) -> Item:
    item = get_owned_item(item_id, user, session)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    item.updated_at = utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> None:
    session.delete(get_owned_item(item_id, user, session))
    session.commit()
