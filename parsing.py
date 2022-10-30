import json
import zlib
import base64

def decode( b64string ):
	decoded_data = base64.b64decode( b64string )
	return zlib.decompress( decoded_data , -15)

def encode( string_val ):
	zlibbed_str = zlib.compress( string_val )
	compressed_string = zlibbed_str[2:-4]
	return base64.b64encode( compressed_string )

def to_data( b64string ):
	inflated_data = decode(b64string)
	return json.loads(inflated_data)

def to_magic( data ):
	stringify = json.dumps(data).encode("utf-8")
	return encode(stringify).decode("utf-8")

def encode_json( data ):
	str = json.dumps(data).encode("utf-8")
	return base64.b64encode(str).decode("utf-8")

def decode_json( data ):
	str = base64.b64decode(data.encode("utf-8"))
	return json.loads(str)
