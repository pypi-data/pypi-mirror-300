from pytorch_lightning.callbacks import DeviceStatsMonitor, EarlyStopping,  \
    ModelSummary, RichModelSummary, RichProgressBar, ModelCheckpoint

# note: keep model_checkpoint as last one, will need to retrieve the best model from it
callback_registry = {
    'device_stats_monitor': DeviceStatsMonitor,
    'early_stopping': EarlyStopping,
    # 'learning_rate_finder': LearningRateFinder,
    # 'learning_rate_monitor': LearningRateMonitor,
    'model_summary': ModelSummary,
    'rich_model_summary': RichModelSummary,
    'rich_progress_bar': RichProgressBar,
    'model_checkpoint': ModelCheckpoint
}


def get_callbacks(params):
    callbacks = []
    for key in params:
        callback_params = params[key] if params[key] else {}
        callback = callback_registry[key](**callback_params)
        callbacks.append(callback)
    return callbacks
