import { Command } from "@oclif/core";

import { saveConfig } from "../../lib/config";
import { runAuthRedirect, serveAuthCode } from "../../lib/service/auth";
import { analyzer } from "../../lib/service/client";

export default class Login extends Command {
  static override description = "describe the command here";

  static override examples = ["<%= config.bin %> <%= command.id %>"];

  static override flags = {};

  static override args = {};

  public async run(): Promise<void> {
    await runAuthRedirect();

    const code = await serveAuthCode(3000);
    this.log(`🔒️ code received:\n  ${code}\n`);

    const credential = await analyzer.public.auth.getCredential.query({ code });
    this.log(`🔐 credential received:\n  ${credential}\n`);
    await saveConfig({ credential });

    const me = await analyzer.protected.me.info.query();
    this.log(`✅ me received:\n  ${JSON.stringify(me)}\n`);

    this.log(
      `🎉 Hi! ${me.displayName}! You are logged in!\n  id: ${me.id}, email: ${me.mail}`
    );
  }
}
