import { Command } from "@oclif/core";
import { readConfig } from "../../lib/config";
import { analyzer } from "../../lib/service/client";

export default class Login extends Command {
  static override description = "describe the command here";

  static override examples = ["<%= config.bin %> <%= command.id %>"];

  static override flags = {};

  static override args = {};

  public async run(): Promise<void> {
    const credential = (await readConfig()).credential;
    const me = await analyzer.protected(credential).me.info.query();

    this.log(JSON.stringify(me));
  }
}
