#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# This example is ported from the SFML C++ examples.

import math
import random

import sfml as sf


def main():
    # Create the window of the application
    window = sf.RenderWindow(sf.VideoMode(800, 600, 32), 'PySFML Pong');

    # Load the sounds used in the game
    ball_sound_buffer = sf.SoundBuffer.load_from_file("resources/ball.wav")
    ball_sound = sf.Sound(ball_sound_buffer);

    # Load the textures used in the game
    background_texture = sf.Texture.load_from_file('resources/background.jpg')
    left_paddle_texture = sf.Texture.load_from_file('resources/paddle_left.png')
    right_paddle_texture = sf.Texture.load_from_file(
        'resources/paddle_right.png')
    ball_texture = sf.Texture.load_from_file('resources/ball.png')

    # Load the text font
    font = sf.Font.load_from_file('resources/sansation.ttf')

    # Initialize the end text
    end = sf.Text()
    end.font = font
    end.character_size = 60
    end.move(150, 200);
    end.color = sf.Color(50, 50, 250)

    # Create the sprites of the background, the paddles and the ball
    background = sf.Sprite(background_texture)
    left_paddle = sf.Sprite(left_paddle_texture)
    right_paddle = sf.Sprite(right_paddle_texture)
    ball = sf.Sprite(ball_texture)

    left_paddle.move(
        10, (window.view.size[1] - left_paddle.global_bounds.height) / 2)
    right_paddle.move(
        window.view.size[0] - right_paddle.global_bounds.width - 10,
        (window.view.size[1] - right_paddle.global_bounds.height) / 2)
    ball.move((window.view.size[0] - ball.global_bounds.width) / 2,
              (window.view.size[1] - ball.global_bounds.height) / 2)

    # Define the paddles properties
    ai_timer = sf.Clock()
    ai_time = sf.Time(milliseconds=100)
    left_paddle_speed  = 0.4
    right_paddle_speed = 0.4

    # Define the ball properties
    ball_speed = 0.4
    ball_angle = 0.0

    clock = sf.Clock()

    while True:
        # Make sure the ball initial angle is not too much vertical
        ball_angle = random.uniform(0.0, 2 * math.pi)

        if abs(math.cos(ball_angle)) < 0.7:
            break

    is_playing = True

    while window.open:
        # Handle events
        for event in window.iter_events():
            # Window closed or escape key pressed : exit
            if ((event.type == sf.Event.CLOSED) or
                (event.type == sf.Event.KEY_PRESSED and
                 event.code == sf.Keyboard.ESCAPE)):
                window.close()
                break

        frame_time = clock.restart().as_milliseconds()

        if is_playing:
            # Move the player's paddle
            if (sf.Keyboard.is_key_pressed(sf.Keyboard.UP) and
                left_paddle.y > 5.0):
                left_paddle.move(0.0, -left_paddle_speed * frame_time)

            if (sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN) and
                (left_paddle.y <
                 window.view.size[1] - left_paddle.global_bounds.height - 5.0)):
                left_paddle.move(0.0, left_paddle_speed * frame_time)

            # Move the computer's paddle
            if (((right_paddle_speed < 0.0) and
                 (right_paddle.y > 5.0)) or
                ((right_paddle_speed > 0.0) and
                 (right_paddle.y < window.view.size[1] -
                  right_paddle.global_bounds.height - 5.0))):
                right_paddle.move(0.0, right_paddle_speed * frame_time)

            # Update the computer's paddle direction according
            # to the ball position
            if ai_timer.elapsed_time > ai_time:
                ai_timer.restart()

                if (right_paddle_speed < 0 and
                    (ball.y + ball.global_bounds.height >
                     right_paddle.y + right_paddle.global_bounds.height)):
                    right_paddle_speed = -right_paddle_speed

                if right_paddle_speed > 0 and ball.y < right_paddle.y:
                    right_paddle_speed = -right_paddle_speed;

            # Move the ball
            factor = ball_speed * frame_time
            ball.move(math.cos(ball_angle) * factor,
                      math.sin(ball_angle) * factor)

            # Check collisions between the ball and the screen
            if ball.x < 0.0:
                is_playing = False
                end.string = "You lost !\n(press escape to exit)"

            if ball.x + ball.global_bounds.width > window.view.size[0]:
                is_playing = False
                end.string = "You won !\n(press escape to exit)"

            if ball.y < 0.0:
                ball_sound.play();
                ball_angle = -ball_angle
                ball.y = 0.1

            if ball.y + ball.global_bounds.height > window.view.size[1]:
                ball_sound.play()
                ball_angle = -ball_angle
                ball.y = window.view.size[1] - ball.global_bounds.height - 0.1

            # Check the collisions between the ball and the paddles
            # Left Paddle
            if (ball.x < left_paddle.x + left_paddle.global_bounds.width and
                ball.x > left_paddle.x +
                (left_paddle.global_bounds.width / 2.0) and
                ball.y + ball.global_bounds.height >= left_paddle.y and
                ball.y <= left_paddle.y + left_paddle.global_bounds.height):
                ball_sound.play()
                ball_angle = math.pi - ball_angle
                ball.x = left_paddle.x + left_paddle.global_bounds.width + 0.1

            # Right Paddle
            if (ball.x + ball.global_bounds.width > right_paddle.x and
                ball.x + ball.global_bounds.width < right_paddle.x +
                (right_paddle.global_bounds.width / 2.0) and
                ball.y + ball.global_bounds.height >= right_paddle.y and
                ball.y <= right_paddle.y + right_paddle.global_bounds.height):
                # ball_sound.play();
                ball_angle = math.pi - ball_angle
                ball.x = right_paddle.x - ball.global_bounds.width - 0.1

        # Clear the window
        window.clear()

        # Draw the background, paddles and ball sprites
        window.draw(background)
        window.draw(left_paddle)
        window.draw(right_paddle)
        window.draw(ball)

        # If the game is over, display the end message
        if not is_playing:
            window.draw(end)

        # Display things on screen
        window.display()


if __name__ == '__main__':
    main()
