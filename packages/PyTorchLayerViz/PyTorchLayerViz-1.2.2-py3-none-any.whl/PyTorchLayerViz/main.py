import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

##########################################################
def extract_layers_and_weights(model, layers_to_check, sequential_order=True):
    # Initialize dictionaries and lists to store layers and their weights
    layer_weights = {}
    layers = {}
    layer_counters = {}
    ordered_layers = []
    ordered_layer_names = []

    # Define the function to add layer info to dictionaries
    def add_layer_info(layer_type, layer):
        if layer_type not in layer_weights:
            layer_weights[layer_type] = []
            layers[layer_type] = []
            layer_counters[layer_type] = 0
        layer_counters[layer_type] += 1
        if hasattr(layer, "weight") and layer.weight is not None:
            layer_weights[layer_type].append(layer.weight)
        layers[layer_type].append(layer)

    # Define the function to add layer info to ordered lists
    def add_ordered_layer_info(layer):
        ordered_layers.append(layer)
        ordered_layer_names.append(type(layer).__name__)

    # Check if the layer type is in the layers_to_check list
    def is_layer_to_check(layer):
        return any(isinstance(layer, layer_class) for layer_class in layers_to_check)

    # Iterate through model's children modules
    for module in model.children():
        if isinstance(module, nn.Sequential):
            for layer in module.children():
                if is_layer_to_check(layer):
                    layer_type = type(layer).__name__
                    if sequential_order:
                        add_ordered_layer_info(layer)
                    else:
                        add_layer_info(layer_type, layer)
        else:
            if is_layer_to_check(module):
                layer_type = type(module).__name__
                if sequential_order:
                    add_ordered_layer_info(module)
                else:
                    add_layer_info(layer_type, module)

    # Print the counts of each layer type
    #    if not sequential_order:
    #        for layer_type, count in layer_counters.items():
    #            print(f"Total {layer_type} layers: {count}")

    if sequential_order:
        return ordered_layers, ordered_layer_names
    else:
        return layer_weights, layers, layer_counters


##########################################################


def extract_feature_maps(layers, input_image):
    feature_maps = []  # List to store feature maps
    layer_names = []  # List to store layer names

    for layer in layers:
        input_image = layer(input_image)
        feature_maps.append(input_image)
        layer_names.append(str(layer))

    return feature_maps, layer_names


##########################################################


def process_feature_maps(feature_maps):
    processed_feature_maps = []  # List to store processed feature maps
    for feature_map in feature_maps:
        feature_map = feature_map.squeeze(0)  # Remove the batch dimension
        if feature_map.shape[0] == 3:
            processed_feature_maps.append(feature_map.data.cpu().numpy())
        else:
            mean_feature_map = torch.sum(feature_map, 0) / feature_map.shape[0]
            processed_feature_maps.append(mean_feature_map.data.cpu().numpy())
    return processed_feature_maps


##########################################################


def apply_colormap(feature_map, cmap="viridis"):
    normed_data = (feature_map - np.min(feature_map)) / (
        np.max(feature_map) - np.min(feature_map)
    )
    colormap = plt.get_cmap(cmap)
    return colormap(normed_data)


##########################################################


def plot_feature_maps(processed_feature_maps, layer_names):
    fig = plt.figure(figsize=(30, 50))
    plot_index = 1
    for i, feature_map in enumerate(processed_feature_maps):
        if feature_map.ndim == 2:
            colored_feature_map = apply_colormap(feature_map)
            ax = fig.add_subplot(5, 4, plot_index)
            ax.imshow(colored_feature_map)
            ax.axis("off")
            ax.set_title(layer_names[i].split("(")[0], fontsize=30)
            plot_index += 1
        elif feature_map.ndim == 3 and feature_map.shape[0] == 3:
            # For RGB, transpose to move channels to the last dimension for plotting
            ax = fig.add_subplot(5, 4, plot_index)
            ax.imshow(np.transpose(feature_map, (1, 2, 0)))
            ax.axis("off")
            ax.set_title(layer_names[i].split("(")[0], fontsize=30)
            plot_index += 1
        else:
            print(f"Skipping feature map at index {i} with shape: {feature_map.shape}")
    plt.show()


##########################################################


def get_feature_maps(
    model, layers_to_check, input_image_path, transform=None, sequential_order=True
):
    if transform is None:
        # Define the image transformations
        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),  # Resize the image to 224x224 pixels
                transforms.ToTensor(),  # Convert the image to a PyTorch tensor
                # transforms.Normalize(mean=0., std=1.)  # Normalize the image tensor
            ]
        )

    # Example usage
    input_image = Image.open(input_image_path)  # add your image path
    input_image = transform(input_image)
    input_image = input_image.unsqueeze(0)  # Add a batch dimension

    if sequential_order:
        ordered_layers, ordered_layer_names = extract_layers_and_weights(
            model, layers_to_check, sequential_order
        )
        feature_maps, layer_names = extract_feature_maps(ordered_layers, input_image)
    else:
        layer_weights, layers, layer_counters = extract_layers_and_weights(
            model, layers_to_check, sequential_order
        )
        feature_maps, layer_names = extract_feature_maps(
            [layer for layer_list in layers.values() for layer in layer_list],
            input_image,
        )

    processed_feature_maps = process_feature_maps(feature_maps)
    plot_feature_maps(processed_feature_maps, layer_names)
    images = []
    for feature_map in processed_feature_maps:
        if feature_map.ndim == 2:  # Grayscale feature map
            colored_feature_map = apply_colormap(feature_map)
            images.append(colored_feature_map)
        elif feature_map.ndim == 3 and feature_map.shape[0] == 3:  # RGB feature map
            images.append(np.transpose(feature_map, (1, 2, 0)))

        return images
