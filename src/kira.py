import kira_args, kira_config, kira_model, kira_project
import sys

kira_config_path = '/home/wyy/code/kira/config/kira.config.json'
has_kira_projext = False

if __name__ == "__main__":
    config = kira_config.Config(kira_config_path)
    args = kira_args.get_args(config)

    if args.init:
        project = kira_project.Project()
        project.new_project()
        sys.exit(0)

    model = kira_model.Model(
       config.model_choice,
       config.models[config.model_choice]['url'],
       config.models[config.model_choice]['v3'],
       config.models[config.model_choice]['r1'],
       config.models[config.model_choice]['key_path'],
       config.models[config.model_choice]['key_key_path'],
       config.models[config.model_choice]['encrypt'],
    )

    has_kira_projext = kira_project.detect_kira()
    project = None
    if has_kira_projext:
       project = kira_project.Project()
       project.set_project()
       model.message.append({
            "role": "system",
            "content": "这是该项目之前的一些问答记录概要\n" + project.history
        })

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

    if has_kira_projext:
        history = ""
        for his in model.history:
            history = history + his + '\n'
        project.write_history(history)

        summary = model.get_summary(history, config)
        project.write_history_summary(summary)
