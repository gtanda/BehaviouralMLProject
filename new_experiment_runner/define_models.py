from tensorflow import keras


class GRU:
    def gru1(input_shape, output_size, activation_function='relu', loss_function="sparse_categorical_crossentropy", optimizer="adam"):
        frame_features_input = keras.Input(input_shape)

        # Refer to the following tutorial to understand the significance of using `mask`:
        # https://keras.io/api/layers/recurrent_layers/gru/
        x = keras.layers.GRU(16, return_sequences=True)(
            frame_features_input
        )
        x = keras.layers.GRU(8)(x)
        x = keras.layers.Dropout(0.4)(x)
        x = keras.layers.Dense(16, activation=activation_function)(x)
        x = keras.layers.Dense(8, activation=activation_function)(x)
        output = keras.layers.Dense(output_size, activation='softmax')(x)

        rnn_model = keras.Model([frame_features_input], output)

        rnn_model.compile(loss=loss_function, optimizer=optimizer, metrics=["accuracy"])

        return rnn_model


    def gru2(input_shape, output_size, activation_function='relu', loss_function="sparse_categorical_crossentropy", optimizer="adam"):
        model = keras.Sequential(
            [
                keras.layers.GRU(16, return_sequences=True),
                keras.layers.GRU(8),
                keras.layers.Dropout(0.4),
                keras.layers.Dense(16, activation=activation_function),
                keras.layers.Dense(8, activation=activation_function),
                keras.layers.Dense(output_size, activation='softmax'),
            ]
        )
