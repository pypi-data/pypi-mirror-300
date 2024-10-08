"""
This module contains the ThreadSafeDict class, which is a thread-safe dictionary.
"""

from threading import RLock
from typing import Any, Optional, List, Iterator


class ThreadSafeDict:
    """
    ThreadSafeDict class to create a thread-safe dictionary.
    """

    def __init__(self):
        self._dict: dict = {}
        self._lock = RLock()

    def __getitem__(self, key: Any) -> Any:
        """
        Get a value from the thread-safe dictionary

        :param Any key: Key to get the value for
        :return: The value from the dictionary
        :rtype: Any
        """
        with self._lock:
            return self._dict[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a key-value pair in the thread-safe dictionary

        :param Any key: Key to set
        :param Any value: Value to set
        :rtype: None
        """
        with self._lock:
            self._dict[key] = value

    def __delitem__(self, key: Any) -> None:
        """
        Delete a key from the thread-safe dictionary

        :param Any key: Key to delete
        :rtype: None
        """
        with self._lock:
            del self._dict[key]

    def get(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Get a value from the thread-safe dictionary

        :param Any key: Key to get the value for
        :param Optional[Any] default: Default value to return if the key is not in the dictionary, defaults to None
        :return: The value from the dictionary, if found or the default value
        :rtype: Optional[Any]
        """
        with self._lock:
            return self._dict.get(key, default)

    def pop(self, key: Any, default: Optional[Any] = None) -> Optional[Any]:
        """
        Pop a value from the thread-safe dictionary

        :param Any key: Key to pop the value for
        :param Optional[Any] default: Default value to return if the key is not in the dictionary, defaults to None
        :return: The value from the dictionary, if found or the default value
        :rtype: Optional[Any]
        """
        with self._lock:
            return self._dict.pop(key, default)

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key is in the thread-safe dictionary

        :param Any key: Key to check in the dictionary
        :return: Whether the key is in the dictionary
        :rtype: bool
        """
        with self._lock:
            return key in self._dict

    def keys(self) -> List[Any]:
        """
        Get a list of keys from the thread-safe dictionary

        :return: A list of keys
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.keys())

    def values(self) -> List[Any]:
        """
        Get a list of values from the thread-safe dictionary

        :return: A list of values
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.values())

    def items(self) -> List[tuple]:
        """
        Get a list of items from the thread-safe dictionary

        :return: A list of items
        :rtype: List[Any]
        """
        with self._lock:
            return list(self._dict.items())

    def clear(self) -> None:
        """
        Clear the thread-safe dictionary

        :rtype: None
        """
        with self._lock:
            self._dict.clear()

    def update(self, other_dict: dict) -> None:
        """
        Update the thread-safe dictionary with another dictionary

        :param dict other_dict: Dictionary to update the thread-safe dictionary with
        :rtype: None
        """
        with self._lock:
            self._dict.update(other_dict)

    def __len__(self) -> int:
        """
        Get the length of the thread-safe dictionary

        :return: The length of the dictionary
        :rtype: int
        """
        with self._lock:
            return len(self._dict)

    def __iter__(self) -> Iterator[Any]:
        """
        Return an iterator over the keys of the dictionary.

        :return: An iterator over the keys of the dictionary
        :rtype: Iterator[Any]
        """
        with self._lock:
            # Create a copy of the keys to prevent issues during iteration
            return iter(self._dict.copy())
