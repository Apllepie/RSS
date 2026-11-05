import os
from launch import LaunchDescription
from launch_ros.actions import Node
from pathlib import Path

PARAM_GENERATOR = Path(__file__).resolve().parent.parent / 'config' / 'generator_params.yaml'
PARAM_SCALER = Path(__file__).resolve().parent.parent / 'config' / 'scaler_params.yaml'

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='signals',
            executable='generator',
            name='generator_node',
            output='screen',
            parameters=[str(PARAM_GENERATOR)]
        ),
        Node(
            package='signals',
            executable='scaler',
            name='scaler_node',
            output='screen',
            parameters=[str(PARAM_SCALER)]
        ),
        Node(
            package='signals',
            executable='visualizer',
            name='visualizer',
            output='screen'
        ),
        Node(
            package='signals',
            executable='visualizer',
            name='visualizer',
            output='screen',
            parameters=[{ 'topic_name': 'scaled_signal_topic' }]
        ),
        # Kolejne węzły możesz dopisać tutaj
    ])