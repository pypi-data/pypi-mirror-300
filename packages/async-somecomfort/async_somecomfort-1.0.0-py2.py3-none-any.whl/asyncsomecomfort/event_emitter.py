"""
This module provides the EventEmitter class, a simple asynchronous event emitter
for managing listeners and emitting events. It allows registration of listeners
that are called when an event is emitted.

Classes:
    EventEmitter: Handles asynchronous event emission and listener management.
"""

import logging

_LOGGER = logging.getLogger(__name__)


class EventEmitter:
    """
    A simple asynchronous event emitter for managing listeners and emitting events.

    Attributes:
        _listeners (list): A list of registered listener functions to be called upon event emission.
    """

    def __init__(self):
        """
        Initializes an empty event emitter with no listeners.
        """
        self._listeners = []

    async def emit(self, *args, **kwargs):
        """
        Asynchronously emits an event to all registered listeners.

        This method will call each listener function with the provided arguments.
        If any listener raises an exception, it will be logged, but will not stop
        the other listeners from being called.

        Args:
            *args: Positional arguments to pass to the listeners.
            **kwargs: Keyword arguments to pass to the listeners.
        """
        _LOGGER.debug("Emitting event: args=%s, kwargs=%s", args, kwargs)
        for listener in self._listeners:
            try:
                await listener(*args, **kwargs)
            except (TypeError, ValueError) as e:
                # Handle specific common errors such as incorrect argument types
                _LOGGER.error("Error in event listener: %s", e)
            except RuntimeError as e:
                # Handle errors related to runtime issues such as event loop problems
                _LOGGER.error("Runtime error in event listener: %s", e)
            except Exception as e:
                # Log any unexpected exception that wasn't handled above
                _LOGGER.error("Unexpected error in event listener: %s", e, exc_info=True)

    def on(self, listener):
        """
        Registers a listener function to be called when an event is emitted.

        The listener should be an asynchronous function. Once registered, it will be
        called with the arguments passed to the `emit` method whenever an event is emitted.

        Args:
            listener (Callable): An asynchronous function to be called when an event is emitted.
        """
        _LOGGER.debug("Adding listener: %s", listener)
        self._listeners.append(listener)

    def off(self, listener):
        """
        Unregisters a previously registered listener function.

        Removes the given listener from the list of listeners, so it will no longer
        be called when an event is emitted.

        Args:
            listener (Callable): The asynchronous function to unregister.
        """
        _LOGGER.debug("Removing listener: %s", listener)
        if listener in self._listeners:
            self._listeners.remove(listener)
        else:
            _LOGGER.warning("Listener %s not found in registered listeners.", listener)
