#!/usr/bin/env python3
"""Strict offline migration of supported Evision events to Vial6 streams."""
import struct


def convert_native_macros(raw):
    if len(raw)!=9472:
        raise ValueError('Native macro storage must be9472 bytes')
    if not any(raw):
        return bytes(16)
    magic,size,count=struct.unpack_from('<HHH',raw)
    if magic!=0x55AA or not 0<=count<=16 or not 16+2*count<=size<=len(raw):
        raise ValueError('Unsupported native macro header; backup is retained')
    if any(raw[6:16]):
        raise ValueError('Native macro header has unknown options')
    streams=[]
    regions=[]
    for index in range(count):
        offset=struct.unpack_from('<H',raw,16+2*index)[0]
        if offset<16+2*count or offset+4>size:
            raise ValueError('Invalid native macro pointer')
        events,options=struct.unpack_from('<HH',raw,offset)
        end=offset+4+events*4
        if options or end>size or any(offset<b and end>a for a,b in regions):
            raise ValueError('Native macro options, overlap, or length is unsupported')
        regions.append((offset,end))
        held=set()
        stream=bytearray()
        for at in range(offset+4,end,4):
            delay,kind,value=struct.unpack_from('<HBB',raw,at)
            down=bool(kind&0x80)
            kind &= 0x7F
            if kind==10 and 4<=value<=0xA4:
                key=value
            elif kind==9 and value and not value&(value-1):
                key=0xE0+value.bit_length()-1
            else:
                raise ValueError('Macro migration supports basic keys and single modifiers only; combined modifier masks need manual re-entry in Vial')
            if down==bool(key in held):
                raise ValueError('Unbalanced native macro event')
            if down:
                held.add(key)
            else:
                held.remove(key)
            stream.extend((1,2 if down else 3,key))
            # Native editor and firmware contract: delay follows the event.
            while delay:
                part=min(delay,65024)
                stream.extend((1,4,(part%255)+1,(part//255)+1))
                delay-=part
        if held:
            raise ValueError('Native macro leaves keys held')
        streams.append(bytes(stream))
    streams.extend([b'']*(16-count))
    result=b''.join(stream+b'\0' for stream in streams)
    if len(result)>9472:
        raise ValueError('Converted macro stream exceeds9472 bytes; reduce it before installing')
    return result
