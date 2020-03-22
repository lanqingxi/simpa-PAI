from ippai.simulate import Tags, SaveFilePaths
from ippai.simulate.models.noise_models import GaussianNoise
from ippai.io_handling.io_hdf5 import save_hdf5, load_hdf5


def apply_noise_model_to_time_series_data(settings, acoustic_model_result_path):
    """

    :param settings:
    :param acoustic_model_result_path:
    :return:
    """

    if not (Tags.APPLY_NOISE_MODEL in settings and settings[Tags.APPLY_NOISE_MODEL]):
        print("WARN: No noise model was applied.")
        return acoustic_model_result_path

    noise_model = None
    time_series_data = load_hdf5(settings[Tags.IPPAI_OUTPUT_PATH], acoustic_model_result_path)[Tags.TIME_SERIES_DATA]

    if settings[Tags.NOISE_MODEL] == Tags.NOISE_MODEL_GAUSSIAN:
        noise_model = GaussianNoise()

    time_series_data_noise = noise_model.apply_noise_model(time_series_data, settings)

    noise_output_path = SaveFilePaths.NOISE_ACOUSTIC_OUTPUT.format("normal", settings[Tags.WAVELENGTH])
    if Tags.PERFORM_UPSAMPLING in settings:
        if settings[Tags.PERFORM_UPSAMPLING]:
            noise_output_path = \
                SaveFilePaths.NOISE_ACOUSTIC_OUTPUT.format("upsampled", settings[Tags.WAVELENGTH])
    save_hdf5({"time_series_data_noise": time_series_data_noise}, settings[Tags.IPPAI_OUTPUT_PATH],
              noise_output_path)

    return noise_output_path


def apply_noise_model_to_reconstructed_data(settings, reconstructed_data_path):
    """
    TODO
    :param settings:
    :param reconstructed_data_path:
    :return:
    """

    if not (Tags.APPLY_NOISE_MODEL in settings and settings[Tags.APPLY_NOISE_MODEL]):
        print("WARN: No noise model was applied.")
        return reconstructed_data_path

    noise_model = None
    reconstructed_data = load_hdf5(settings[Tags.IPPAI_OUTPUT_PATH], reconstructed_data_path)[Tags.RECONSTRUCTED_DATA]

    if settings[Tags.NOISE_MODEL] == Tags.NOISE_MODEL_GAUSSIAN:
        noise_model = GaussianNoise()

    reconstructed_data_noise = noise_model.apply_noise_model(reconstructed_data, settings)

    noise_output_path = SaveFilePaths.NOISE_RECONSTRCTION_OUTPUT.format("normal", settings[Tags.WAVELENGTH])
    if Tags.PERFORM_UPSAMPLING in settings:
        if settings[Tags.PERFORM_UPSAMPLING]:
            noise_output_path = \
                SaveFilePaths.NOISE_RECONSTRCTION_OUTPUT.format("upsampled", settings[Tags.WAVELENGTH])
    save_hdf5({"reconstructed_data_noise": reconstructed_data_noise}, settings[Tags.IPPAI_OUTPUT_PATH],
              noise_output_path)

    return noise_output_path
