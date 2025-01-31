from unittest.mock import AsyncMock
from warnings import deprecated


class User:
	id: int = 1

	def to_primitives(self):
		return {"id": 1, "name": "John Doe"}


class UserRepository:
	async def save(self, user: User) -> None:
		raise NotImplementedError

	async def search(self, user_id: int) -> User:
		raise NotImplementedError


class UserRegistrar:
	def __init__(self, repository: UserRepository) -> None:
		self.repository = repository

	async def save(self, user: User) -> None:
		await self.repository.save(user)

	async def search(self, user_id: int) -> User:
		return await self.repository.search(user_id)


class MockUserRepository(UserRepository):
	def __init__(self):
		self.mock_save = AsyncMock()
		self.mock_search = AsyncMock()

	async def save(self, user: User) -> None:
		self.mock_save.assert_called_with(user.to_primitives())

	async def search(self, user_id: int) -> User:
		self.mock_search.assert_called_with(user_id)
		return await self.mock_search()

	def should_save(self, user: User) -> None:
		"""
		This simply calls the mock_save function with user.to_primitives(),
		like the TypeScript example's 'shouldSave' method.
		"""
		self.mock_save(user.to_primitives())

	def should_search(self, user_id: int) -> None:
		"""
		This simply calls the mock_search function with user_id,
		like the TypeScript example's 'shouldSearch' method.
		"""
		self.mock_search(user_id)
		self.mock_search.return_value = User()

import pytest


@pytest.mark.asyncio
class TestUser:
	async def test_save_user(self):
		user = User()
		mock_user_repository = MockUserRepository()
		register = UserRegistrar(mock_user_repository)

		mock_user_repository.should_save(user)

		await register.save(user)

	async def test_search_user(self):
		expected_user = User()
		mock_user_repository = MockUserRepository()
		register = UserRegistrar(mock_user_repository)

		mock_user_repository.should_search(expected_user.id)

		user = await register.search(expected_user.id)

		assert user.to_primitives() == expected_user.to_primitives()
