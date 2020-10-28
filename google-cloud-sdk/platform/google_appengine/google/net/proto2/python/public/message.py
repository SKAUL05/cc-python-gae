#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#








"""Contains an abstract base class for protocol messages."""



class Error(Exception):
  """Base error type for this module."""
  pass


class DecodeError(Error):
  """Exception raised when deserializing messages."""
  pass


class EncodeError(Error):
  """Exception raised when serializing messages."""
  pass


class Message(object):

  """Abstract base class for protocol messages.

  Protocol message classes are almost always generated by the protocol
  compiler.  These generated types subclass Message and implement the methods
  shown below.
  """













  __slots__ = []


  DESCRIPTOR = None

  def __deepcopy__(self, memo=None):
    clone = type(self)()
    clone.MergeFrom(self)
    return clone

  def __eq__(self, other_msg):
    """Recursively compares two messages by value and structure."""
    raise NotImplementedError

  def __ne__(self, other_msg):

    return not self == other_msg

  def __hash__(self):
    raise TypeError('unhashable object')

  def __str__(self):
    """Outputs a human-readable representation of the message."""
    raise NotImplementedError

  def __unicode__(self):
    """Outputs a human-readable representation of the message."""
    raise NotImplementedError

  def MergeFrom(self, other_msg):
    """Merges the contents of the specified message into current message.

    This method merges the contents of the specified message into the current
    message. Singular fields that are set in the specified message overwrite
    the corresponding fields in the current message. Repeated fields are
    appended. Singular sub-messages and groups are recursively merged.

    Args:
      other_msg (Message): A message to merge into the current message.
    """
    raise NotImplementedError

  def CopyFrom(self, other_msg):
    """Copies the content of the specified message into the current message.

    The method clears the current message and then merges the specified
    message using MergeFrom.

    Args:
      other_msg (Message): A message to copy into the current one.
    """
    if self is other_msg:
      return
    self.Clear()
    self.MergeFrom(other_msg)

  def Clear(self):
    """Clears all data that was set in the message."""
    raise NotImplementedError

  def SetInParent(self):
    """Mark this as present in the parent.

    This normally happens automatically when you assign a field of a
    sub-message, but sometimes you want to make the sub-message
    present while keeping it empty.  If you find yourself using this,
    you may want to reconsider your design.
    """
    raise NotImplementedError

  def IsInitialized(self):
    """Checks if the message is initialized.

    Returns:
      bool: The method returns True if the message is initialized (i.e. all of
      its required fields are set).
    """
    raise NotImplementedError







  def MergeFromString(self, serialized):
    """Merges serialized protocol buffer data into this message.

    When we find a field in `serialized` that is already present
    in this message:

    -   If it's a "repeated" field, we append to the end of our list.
    -   Else, if it's a scalar, we overwrite our field.
    -   Else, (it's a nonrepeated composite), we recursively merge
        into the existing composite.

    Args:
      serialized (bytes): Any object that allows us to call
        ``memoryview(serialized)`` to access a string of bytes using the
        buffer interface.

    Returns:
      int: The number of bytes read from `serialized`.
      For non-group messages, this will always be `len(serialized)`,
      but for messages which are actually groups, this will
      generally be less than `len(serialized)`, since we must
      stop when we reach an ``END_GROUP`` tag.  Note that if
      we *do* stop because of an ``END_GROUP`` tag, the number
      of bytes returned does not include the bytes
      for the ``END_GROUP`` tag information.

    Raises:
      DecodeError: if the input cannot be parsed.
    """


    raise NotImplementedError

  def ParseFromString(self, serialized):
    """Parse serialized protocol buffer data into this message.

    Like :func:`MergeFromString()`, except we clear the object first.
    """
    self.Clear()
    return self.MergeFromString(serialized)

  def SerializeToString(self, **kwargs):
    """Serializes the protocol message to a binary string.

    Keyword Args:
      deterministic (bool): If true, requests deterministic serialization
        of the protobuf, with predictable ordering of map keys.

    Returns:
      A binary string representation of the message if all of the required
      fields in the message are set (i.e. the message is initialized).

    Raises:
      EncodeError: if the message isn't initialized (see :func:`IsInitialized`).
    """
    raise NotImplementedError

  def SerializePartialToString(self, **kwargs):
    """Serializes the protocol message to a binary string.

    This method is similar to SerializeToString but doesn't check if the
    message is initialized.

    Keyword Args:
      deterministic (bool): If true, requests deterministic serialization
        of the protobuf, with predictable ordering of map keys.

    Returns:
      bytes: A serialized representation of the partial message.
    """
    raise NotImplementedError

















  def ListFields(self):
    """Returns a list of (FieldDescriptor, value) tuples for present fields.

    A message field is non-empty if HasField() would return true. A singular
    primitive field is non-empty if HasField() would return true in proto2 or it
    is non zero in proto3. A repeated field is non-empty if it contains at least
    one element. The fields are ordered by field number.

    Returns:
      list[tuple(FieldDescriptor, value)]: field descriptors and values
      for all fields in the message which are not empty. The values vary by
      field type.
    """
    raise NotImplementedError

  def HasField(self, field_name):
    """Checks if a certain field is set for the message.

    For a oneof group, checks if any field inside is set. Note that if the
    field_name is not defined in the message descriptor, :exc:`ValueError` will
    be raised.

    Args:
      field_name (str): The name of the field to check for presence.

    Returns:
      bool: Whether a value has been set for the named field.

    Raises:
      ValueError: if the `field_name` is not a member of this message.
    """
    raise NotImplementedError

  def ClearField(self, field_name):
    """Clears the contents of a given field.

    Inside a oneof group, clears the field set. If the name neither refers to a
    defined field or oneof group, :exc:`ValueError` is raised.

    Args:
      field_name (str): The name of the field to check for presence.

    Raises:
      ValueError: if the `field_name` is not a member of this message.
    """
    raise NotImplementedError

  def WhichOneof(self, oneof_group):
    """Returns the name of the field that is set inside a oneof group.

    If no field is set, returns None.

    Args:
      oneof_group (str): the name of the oneof group to check.

    Returns:
      str or None: The name of the group that is set, or None.

    Raises:
      ValueError: no group with the given name exists
    """
    raise NotImplementedError

  def HasExtension(self, extension_handle):
    """Checks if a certain extension is present for this message.

    Extensions are retrieved using the :attr:`Extensions` mapping (if present).

    Args:
      extension_handle: The handle for the extension to check.

    Returns:
      bool: Whether the extension is present for this message.

    Raises:
      KeyError: if the extension is repeated. Similar to repeated fields,
        there is no separate notion of presence: a "not present" repeated
        extension is an empty list.
    """
    raise NotImplementedError

  def ClearExtension(self, extension_handle):
    """Clears the contents of a given extension.

    Args:
      extension_handle: The handle for the extension to clear.
    """
    raise NotImplementedError

  def UnknownFields(self):
    """Returns the UnknownFieldSet.

    Returns:
      UnknownFieldSet: The unknown fields stored in this message.
    """
    raise NotImplementedError

  def DiscardUnknownFields(self):
    """Clears all fields in the :class:`UnknownFieldSet`.

    This operation is recursive for nested message.
    """
    raise NotImplementedError

  def ByteSize(self):
    """Returns the serialized size of this message.

    Recursively calls ByteSize() on all contained messages.

    Returns:
      int: The number of bytes required to serialize this message.
    """
    raise NotImplementedError

  def _SetListener(self, message_listener):
    """Internal method used by the protocol message implementation.
    Clients should not call this directly.

    Sets a listener that this message will call on certain state transitions.

    The purpose of this method is to register back-edges from children to
    parents at runtime, for the purpose of setting "has" bits and
    byte-size-dirty bits in the parent and ancestor objects whenever a child or
    descendant object is modified.

    If the client wants to disconnect this Message from the object tree, she
    explicitly sets callback to None.

    If message_listener is None, unregisters any existing listener.  Otherwise,
    message_listener must implement the MessageListener interface in
    internal/message_listener.py, and we discard any listener registered
    via a previous _SetListener() call.
    """
    raise NotImplementedError

  def __getstate__(self):
    """Support the pickle protocol."""
    return dict(serialized=self.SerializePartialToString())

  def __setstate__(self, state):
    """Support the pickle protocol."""
    self.__init__()
    serialized = state['serialized']


    if not isinstance(serialized, bytes):
      serialized = serialized.encode('latin1')
    self.ParseFromString(serialized)

  def __reduce__(self):
    message_descriptor = self.DESCRIPTOR
    if message_descriptor.containing_type is None:
      return type(self), (), self.__getstate__()



    container = message_descriptor
    return (_InternalConstructMessage, (container.full_name,),
            self.__getstate__())


def _InternalConstructMessage(full_name):
  """Constructs a nested message."""
  from google.net.proto2.python.public import symbol_database

  return symbol_database.Default().GetSymbol(full_name)()