import { Command } from "@oclif/core";
import { runAuthRedirect } from "../../lib/service/auth";

export default class Login extends Command {
  static override description = "describe the command here";

  static override examples = ["<%= config.bin %> <%= command.id %>"];

  static override flags = {};

  static override args = {};

  public async run(): Promise<void> {
    runAuthRedirect();
    // const result = await client.public.auth.getCredential.query({ code: "" });
    // this.log(result);
  }
}
