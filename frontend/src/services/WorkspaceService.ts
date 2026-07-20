import * as vscode from "vscode";

export interface WorkspaceContext {

    projectName: string;

    files: string[];

    folders: string[];

    tree: string;

}

export class WorkspaceService {

    static async getContext(): Promise<WorkspaceContext> {

        const workspace =
            vscode.workspace.workspaceFolders?.[0];

        if (!workspace) {

            return {

                projectName: "",

                files: [],

                folders: [],

                tree: ""

            };

        }

        const files: string[] = [];
        const folders: string[] = [];

        const tree = await this.buildTree(

            workspace.uri,

            "",

            files,

            folders

        );

        return {

            projectName: workspace.name,

            files,

            folders,

            tree

        };

    }

    private static async buildTree(

        uri: vscode.Uri,

        indent: string,

        files: string[],

        folders: string[]

    ): Promise<string> {

        let result = "";

        const entries = await vscode.workspace.fs.readDirectory(uri);

        entries.sort((a, b) => {

            if (a[1] === b[1])

                return a[0].localeCompare(b[0]);

            return a[1] === vscode.FileType.Directory ? -1 : 1;

        });

        for (const [name, type] of entries) {

        if (

            name === ".git" ||

            name === ".github" ||

            name === ".vscode" ||

            name === ".venv" ||

            name === "venv" ||

            name === "__pycache__" ||

            name === "node_modules" ||

            name === "dist" ||

            name === "build" ||

            name === ".next" ||

            name === ".pytest_cache" ||

            name === ".mypy_cache"

        ){

            continue;

        }

            if (type === vscode.FileType.Directory) {

                folders.push(name);

                result += `${indent}📁 ${name}\n`;

                result += await this.buildTree(

                    vscode.Uri.joinPath(uri, name),

                    indent + "    ",

                    files,

                    folders

                );

            }

            else {

                files.push(name);

                result += `${indent}📄 ${name}\n`;

            }

        }

        return result;

    }

}