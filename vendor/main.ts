import { SSF } from "my_ssf";

function convertStringToType(
    value: string | null,
): string | number | boolean | null {
    // handle null and empty strings
    if (value === null) return null;
    if (value.trim() === "") return value;

    // Try to convert to number
    const num = Number(value);
    if (!isNaN(num)) {
        return num;
    }

    // Try to convert to boolean
    if (value.toLowerCase() === "true") return true;
    if (value.toLowerCase() === "false") return false;

    return value;
}

if (Deno.args.length < 2) {
    Deno.stderr.write(
        new TextEncoder().encode("Error: format and value must be provided.\n"),
    );
    Deno.exit(1);
}

const format: string = Deno.args[0];
const value: string | number | boolean | null = Deno.args[1];
const options: object = Deno.args[2] ? JSON.parse(Deno.args[2]) : {};

const convertedValue = convertStringToType(value);

try {
    console.log(SSF.format(format, convertedValue, options));
} catch (e) {
    if (e instanceof Error) {
        Deno.stderr.write(
            new TextEncoder().encode(
                `Error calling SSF.format: ${e.message}\n`,
            ),
        );
    } else {
        Deno.stderr.write(
            new TextEncoder().encode(
                `An unknown error occurred during formatting.\n`,
            ),
        );
    }
    Deno.exit(1);
}
