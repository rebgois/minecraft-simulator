from PIL import Image
import os
import wave
import math

def create_texture(name, color):
    # Cria uma imagem 64x64 com a cor especificada
    img = Image.new('RGB', (64, 64), color)
    
    # Cria o diretório de texturas se não existir
    if not os.path.exists('textures'):
        os.makedirs('textures')
    
    # Salva a imagem
    img.save(f'textures/{name}.png')

def create_sound():
    # Cria um arquivo WAV com um beep simples
    sample_rate = 44100
    duration = 0.1  # 100ms
    frequency = 440.0  # 440 Hz
    amplitude = 32767.0

    num_samples = int(duration * sample_rate)
    audio_data = []

    for i in range(num_samples):
        t = float(i) / sample_rate
        value = int(amplitude * math.sin(2.0 * math.pi * frequency * t))
        # Garantir que o valor está dentro dos limites
        value = max(-32767, min(32767, value))
        audio_data.append(value)

    with wave.open('textures/punch_sound.wav', 'w') as wavefile:
        wavefile.setnchannels(1)  # mono
        wavefile.setsampwidth(2)  # 2 bytes por amostra
        wavefile.setframerate(sample_rate)
        
        # Converter os valores para bytes
        import struct
        packed_data = struct.pack('<%dh' % len(audio_data), *audio_data)
        wavefile.writeframes(packed_data)

# Cria texturas básicas
create_texture('grass_block', '#5ab552')  # Verde para grama
create_texture('stone_block', '#828282')  # Cinza para pedra
create_texture('brick_block', '#963c3c')  # Vermelho para tijolo
create_texture('skybox', '#87ceeb')       # Azul claro para o céu
create_texture('arm_texture', '#ffd700')   # Dourado para a arma

# Cria o arquivo de som
create_sound() 