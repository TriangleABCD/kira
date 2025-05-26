import kira_args, kira_config, kira_model

kira_config_path = '/home/wyy/code/kira/config/kira.config.json'


if __name__ == "__main__":
    config = kira_config.Config(kira_config_path)
    args = kira_args.get_args(config)

    model = kira_model.Model(
       config.model_choice,
       config.models[config.model_choice]['url'],
       config.models[config.model_choice]['v3'],
       config.models[config.model_choice]['r1'],
       config.models[config.model_choice]['key_path'],
       config.models[config.model_choice]['key_key_path'],
       config.models[config.model_choice]['encrypt'],
    )

    if args.chat:
        if args.model == config.models[config.model_choice]['v3']:
            model.chat(args, config)
        else:
            model.reasonal_chat(args, config)
    else:
        if args.model == config.models[config.model_choice]['v3']:
            model.chat_once(args, config)
        else:
            model.reasonal_chat_once(args, config)
