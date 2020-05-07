# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chunk.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chunk.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0b\x63hunk.proto\"3\n\x05\x43hunk\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0c\n\x04loss\x18\x03 \x01(\x02\"\x17\n\x07Request\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x17\n\x05Reply\x12\x0e\n\x06length\x18\x01 \x01(\x05\x32X\n\nFileServer\x12\"\n\x0cupload_model\x12\x06.Chunk\x1a\x06.Reply\"\x00(\x01\x12&\n\x0e\x64ownload_model\x12\x08.Request\x1a\x06.Chunk\"\x00\x30\x01\x62\x06proto3'
)




_CHUNK = _descriptor.Descriptor(
  name='Chunk',
  full_name='Chunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buffer', full_name='Chunk.buffer', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='Chunk.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loss', full_name='Chunk.loss', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=66,
)


_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Request.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=91,
)


_REPLY = _descriptor.Descriptor(
  name='Reply',
  full_name='Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='length', full_name='Reply.length', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=93,
  serialized_end=116,
)

DESCRIPTOR.message_types_by_name['Chunk'] = _CHUNK
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['Reply'] = _REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Chunk = _reflection.GeneratedProtocolMessageType('Chunk', (_message.Message,), {
  'DESCRIPTOR' : _CHUNK,
  '__module__' : 'chunk_pb2'
  # @@protoc_insertion_point(class_scope:Chunk)
  })
_sym_db.RegisterMessage(Chunk)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'chunk_pb2'
  # @@protoc_insertion_point(class_scope:Request)
  })
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'chunk_pb2'
  # @@protoc_insertion_point(class_scope:Reply)
  })
_sym_db.RegisterMessage(Reply)



_FILESERVER = _descriptor.ServiceDescriptor(
  name='FileServer',
  full_name='FileServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=118,
  serialized_end=206,
  methods=[
  _descriptor.MethodDescriptor(
    name='upload_model',
    full_name='FileServer.upload_model',
    index=0,
    containing_service=None,
    input_type=_CHUNK,
    output_type=_REPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='download_model',
    full_name='FileServer.download_model',
    index=1,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_CHUNK,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_FILESERVER)

DESCRIPTOR.services_by_name['FileServer'] = _FILESERVER

# @@protoc_insertion_point(module_scope)