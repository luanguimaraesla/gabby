"""
Module to handle message serialization
"""
import struct
import logging

def encode(message, fmt):
    return struct.pack(fmt, *message.data)
