import { Command } from "@oclif/core";
import { readConfig, saveConfig } from "../../lib/config";

export default class Login extends Command {
  static override description = "describe the command here";

  static override examples = ["<%= config.bin %> <%= command.id %>"];

  static override flags = {};

  static override args = {};

  public async run(): Promise<void> {
    await saveConfig({ credential: "credential" });

    console.log(await readConfig());
  }
}
