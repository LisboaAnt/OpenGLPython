from renderer import Renderer

def main():
    renderer = Renderer(800, 600, "Triângulo Simples")
    
    # Apenas um triângulo
    renderer.adicionar_triangulo()
    
    try:
        renderer.executar()
    finally:
        renderer.cleanup()

if __name__ == "__main__":
    main()
