import os
import sys
import webbrowser
import subprocess

def create_standalone_html():
    """Create a standalone HTML file with the game"""
    print("Creating standalone HTML file...")
    
    # Create the build directory if it doesn't exist
    os.makedirs("build/web", exist_ok=True)
    
    # HTML content with the game
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kids Car Racing Adventure</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #87CEEB;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
        }
        
        #game-container {
            width: 800px;
            height: 600px;
            max-width: 100%;
            max-height: 80vh;
            position: relative;
            border: 2px solid #333;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        canvas {
            width: 100%;
            height: 100%;
            display: block;
        }
        
        .touch-controls {
            position: absolute;
            bottom: 20px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            padding: 0 20px;
            box-sizing: border-box;
        }
        
        .control-button {
            width: 80px;
            height: 80px;
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
        }
        
        .arrow {
            width: 0;
            height: 0;
            border-top: 15px solid transparent;
            border-bottom: 15px solid transparent;
        }
        
        .arrow-left {
            border-right: 25px solid #333;
        }
        
        .arrow-right {
            border-left: 25px solid #333;
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .instructions {
            background-color: #fff;
            padding: 15px;
            border-radius: 10px;
            margin: 20px;
            max-width: 600px;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Kids Car Racing Adventure</h1>
    
    <div class="instructions">
        <p>Use LEFT and RIGHT arrow keys or touch buttons to control your car.</p>
        <p>Avoid other cars to score points! You have 4 lives.</p>
    </div>
    
    <div id="game-container">
        <canvas id="game-canvas"></canvas>
        <div class="touch-controls">
            <div class="control-button" id="left-button">
                <div class="arrow arrow-left"></div>
            </div>
            <div class="control-button" id="right-button">
                <div class="arrow arrow-right"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Simple game implementation
        document.addEventListener('DOMContentLoaded', function() {
            const canvas = document.getElementById('game-canvas');
            const ctx = canvas.getContext('2d');
            const leftButton = document.getElementById('left-button');
            const rightButton = document.getElementById('right-button');
            
            // Set canvas dimensions
            canvas.width = 800;
            canvas.height = 600;
            
            // Game variables
            let playerX = canvas.width / 2 - 25;
            const playerY = canvas.height - 100;
            const playerWidth = 50;
            const playerHeight = 80;
            const playerSpeed = 5;
            
            let score = 0;
            let lives = 4;
            let gameOver = false;
            
            // Control states
            let leftPressed = false;
            let rightPressed = false;
            
            // Enemy cars
            const enemies = [];
            const enemyWidth = 50;
            const enemyHeight = 80;
            
            // Create initial enemies
            for (let i = 0; i < 3; i++) {
                enemies.push({
                    x: Math.random() * (canvas.width - 300) + 150,
                    y: -100 - Math.random() * 400,
                    speed: 2 + Math.random() * 3,
                    color: ['blue', 'green', 'orange'][Math.floor(Math.random() * 3)]
                });
            }
            
            // Event listeners for keyboard
            document.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowLeft') leftPressed = true;
                if (e.key === 'ArrowRight') rightPressed = true;
                if (e.key === ' ' && gameOver) resetGame();
            });
            
            document.addEventListener('keyup', function(e) {
                if (e.key === 'ArrowLeft') leftPressed = false;
                if (e.key === 'ArrowRight') rightPressed = false;
            });
            
            // Event listeners for touch controls
            leftButton.addEventListener('touchstart', function(e) {
                e.preventDefault();
                leftPressed = true;
            });
            
            leftButton.addEventListener('touchend', function(e) {
                e.preventDefault();
                leftPressed = false;
            });
            
            rightButton.addEventListener('touchstart', function(e) {
                e.preventDefault();
                rightPressed = true;
            });
            
            rightButton.addEventListener('touchend', function(e) {
                e.preventDefault();
                rightPressed = false;
            });
            
            // Also handle mouse events for testing on desktop
            leftButton.addEventListener('mousedown', function() {
                leftPressed = true;
            });
            
            leftButton.addEventListener('mouseup', function() {
                leftPressed = false;
            });
            
            leftButton.addEventListener('mouseleave', function() {
                leftPressed = false;
            });
            
            rightButton.addEventListener('mousedown', function() {
                rightPressed = true;
            });
            
            rightButton.addEventListener('mouseup', function() {
                rightPressed = false;
            });
            
            rightButton.addEventListener('mouseleave', function() {
                rightPressed = false;
            });
            
            // Canvas click for restart
            canvas.addEventListener('click', function() {
                if (gameOver) resetGame();
            });
            
            function resetGame() {
                playerX = canvas.width / 2 - 25;
                score = 0;
                lives = 4;
                gameOver = false;
                
                // Reset enemies
                enemies.length = 0;
                for (let i = 0; i < 3; i++) {
                    enemies.push({
                        x: Math.random() * (canvas.width - 300) + 150,
                        y: -100 - Math.random() * 400,
                        speed: 2 + Math.random() * 3,
                        color: ['blue', 'green', 'orange'][Math.floor(Math.random() * 3)]
                    });
                }
            }
            
            function drawRoad() {
                // Sky
                ctx.fillStyle = '#87CEEB';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Road
                ctx.fillStyle = '#555';
                ctx.fillRect(150, 0, canvas.width - 300, canvas.height);
                
                // Road edges
                ctx.fillStyle = '#FFF';
                ctx.fillRect(150, 0, 5, canvas.height);
                ctx.fillRect(canvas.width - 155, 0, 5, canvas.height);
                
                // Lane markings
                ctx.fillStyle = '#FFF';
                for (let y = -50 + (Date.now() / 50) % 80; y < canvas.height; y += 80) {
                    ctx.fillRect(canvas.width / 2 - 5, y, 10, 40);
                }
                
                // Grass
                ctx.fillStyle = '#0A0';
                ctx.fillRect(0, 0, 150, canvas.height);
                ctx.fillRect(canvas.width - 150, 0, 150, canvas.height);
            }
            
            function drawPlayer() {
                // Car body
                ctx.fillStyle = '#F00';
                ctx.fillRect(playerX, playerY, playerWidth, playerHeight);
                
                // Windows
                ctx.fillStyle = '#ADF';
                ctx.fillRect(playerX + 5, playerY + 5, playerWidth - 10, 20);
                
                // Wheels
                ctx.fillStyle = '#000';
                ctx.fillRect(playerX - 5, playerY + 10, 5, 15);
                ctx.fillRect(playerX - 5, playerY + 55, 5, 15);
                ctx.fillRect(playerX + playerWidth, playerY + 10, 5, 15);
                ctx.fillRect(playerX + playerWidth, playerY + 55, 5, 15);
            }
            
            function drawEnemies() {
                enemies.forEach(enemy => {
                    // Car body
                    ctx.fillStyle = enemy.color;
                    ctx.fillRect(enemy.x, enemy.y, enemyWidth, enemyHeight);
                    
                    // Windows
                    ctx.fillStyle = '#ADF';
                    ctx.fillRect(enemy.x + 5, enemy.y + 5, enemyWidth - 10, 20);
                    
                    // Wheels
                    ctx.fillStyle = '#000';
                    ctx.fillRect(enemy.x - 5, enemy.y + 10, 5, 15);
                    ctx.fillRect(enemy.x - 5, enemy.y + 55, 5, 15);
                    ctx.fillRect(enemy.x + enemyWidth, enemy.y + 10, 5, 15);
                    ctx.fillRect(enemy.x + enemyWidth, enemy.y + 55, 5, 15);
                });
            }
            
            function drawUI() {
                ctx.fillStyle = '#000';
                ctx.font = '24px Arial';
                ctx.fillText(`Score: ${score}`, 20, 30);
                
                // Draw lives
                ctx.fillStyle = '#F00';
                for (let i = 0; i < lives; i++) {
                    ctx.fillRect(canvas.width - 40 - i * 30, 20, 20, 20);
                }
                
                if (gameOver) {
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    ctx.fillStyle = '#FFF';
                    ctx.font = '48px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 40);
                    ctx.font = '24px Arial';
                    ctx.fillText(`Final Score: ${score}`, canvas.width / 2, canvas.height / 2 + 20);
                    ctx.fillText('Tap or click to restart', canvas.width / 2, canvas.height / 2 + 60);
                    ctx.textAlign = 'left';
                }
            }
            
            function checkCollisions() {
                if (gameOver) return;
                
                for (const enemy of enemies) {
                    if (
                        playerX < enemy.x + enemyWidth &&
                        playerX + playerWidth > enemy.x &&
                        playerY < enemy.y + enemyHeight &&
                        playerY + playerHeight > enemy.y
                    ) {
                        // Collision detected
                        lives--;
                        
                        // Reset enemy position
                        enemy.y = -100 - Math.random() * 200;
                        enemy.x = Math.random() * (canvas.width - 300) + 150;
                        
                        if (lives <= 0) {
                            gameOver = true;
                        }
                        
                        break;
                    }
                }
            }
            
            function update() {
                if (!gameOver) {
                    // Update player position
                    if (leftPressed && playerX > 155) {
                        playerX -= playerSpeed;
                    }
                    if (rightPressed && playerX < canvas.width - 155 - playerWidth) {
                        playerX += playerSpeed;
                    }
                    
                    // Update enemies
                    enemies.forEach(enemy => {
                        enemy.y += enemy.speed;
                        
                        // Reset enemy when it goes off screen
                        if (enemy.y > canvas.height) {
                            enemy.y = -100 - Math.random() * 200;
                            enemy.x = Math.random() * (canvas.width - 300) + 150;
                            enemy.speed = 2 + Math.random() * 3;
                            enemy.color = ['blue', 'green', 'orange'][Math.floor(Math.random() * 3)];
                            
                            // Increase score
                            score += 10;
                        }
                    });
                    
                    // Check for collisions
                    checkCollisions();
                }
            }
            
            function gameLoop() {
                update();
                
                // Draw everything
                drawRoad();
                drawEnemies();
                drawPlayer();
                drawUI();
                
                requestAnimationFrame(gameLoop);
            }
            
            // Start the game loop
            gameLoop();
        });
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open("build/web/index.html", "w") as f:
        f.write(html_content)
    
    print("Standalone HTML file created successfully!")
    return True

def start_local_server():
    """Start a local web server to test the game"""
    print("\nStarting local web server...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "build", "web")
    
    # Check if build directory exists
    if not os.path.exists(build_dir):
        print(f"Error: Build directory not found at {build_dir}")
        return False
    
    # Change to the build directory
    os.chdir(build_dir)
    
    # Determine an available port
    port = 8000
    
    print(f"Starting server at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{port}")
    
    # Start the server
    try:
        # Use the http.server module
        server_command = [sys.executable, "-m", "http.server", str(port)]
        subprocess.run(server_command)
        return True
    except KeyboardInterrupt:
        print("\nServer stopped")
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        return False

def main():
    print("===== Simple Car Racing Game Web Version =====")
    
    # Create standalone HTML file
    create_standalone_html()
    
    # Start local server
    start_local_server()

if __name__ == "__main__":
    main()