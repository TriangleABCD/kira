import kira_args, kira_config, kira_model


if __name__ == "__main__":
    config = kira_config.Config('/home/wyy/code/kira/config/kira.config.json')
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
    
    message = model.message
    message.append({"role": "user", "content": "解释什么是伙伴系统"})

    response = model.client.chat.completions.create(
        model=config.models[config.model_choice]['v3'],
        messages=message,
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
