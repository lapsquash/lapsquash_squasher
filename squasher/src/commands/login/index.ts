import { Args, Command, Flags } from "@oclif/core";
import { client } from "../../lib/service/client";

export default class Login extends Command {
  static description = "Say hell o";

  static examples = [
    `$ oex hello friend --from oclif
hello friend from oclif! (./src/commands/hello/index.ts)
`,
  ];

  static flags = {
    from: Flags.string({
      char: "f",
      description: "Who is saying hello",
      required: true,
    }),
  };

  static args = {
    person: Args.string({
      description: "Person to say hello to",
      required: true,
    }),
  };

  async run(): Promise<void> {
    const result = await client.auth.getCredential.query({
      code: "",
    });
    this.log(result);
    this.log("howdy");
  }
}
