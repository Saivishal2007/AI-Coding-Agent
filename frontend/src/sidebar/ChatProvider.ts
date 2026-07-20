import * as fs from "fs";
import * as vscode from "vscode";
import { BackendService } from "../services/BackendService";
import { WorkspaceService } from "../services/WorkspaceService";
import { randomUUID } from "crypto";
interface EditorContext {

    workspace: any;

    active_file: string;

    language: string;

    selected_text: string;

}

export class ChatProvider implements vscode.WebviewViewProvider {

    public static readonly viewType = "aiCodingAgent.chatView";
    private readonly sessionId = randomUUID();
    constructor(
        private readonly extensionUri: vscode.Uri
    ) {}

    resolveWebviewView(webviewView: vscode.WebviewView) {

        console.log("resolveWebviewView called");

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [
                vscode.Uri.joinPath(this.extensionUri, "media")
            ]
        };

        webviewView.webview.html = this.getHtml(webviewView.webview);


        webviewView.webview.onDidReceiveMessage(async (message) => {
            if (message.command === "applyEdit") {

                try {

                    const result =
                        await BackendService.applyEdit(message.editId);

                    console.log(result);

                    // Refresh the currently opened file
                    const editor = vscode.window.activeTextEditor;

                    if (editor) {

                        // await editor.document.save();

                        // await vscode.commands.executeCommand(
                            // "workbench.action.files.revert"
                        // );

                    }

                    vscode.window.showInformationMessage(
                        "✅ Edit applied successfully."
                    );

                    webviewView.webview.postMessage({

                        type: "apply_success",

                    });

                } catch (error: any) {

                    webviewView.webview.postMessage({

                        type: "response",

                        response: error.message

                    });

                }

                return;

            }
            if (message.command === "sendPrompt") {

                try {

                    const editor = vscode.window.activeTextEditor;

                    const workspaceContext =
                            await WorkspaceService.getContext();

                        let context: EditorContext = {

                            workspace: workspaceContext,

                            active_file: "",

                            language: "",

                            selected_text: ""

                        };

                        if (editor) {

                            const selection = editor.selection;

                            const selectedText =
                                editor.document.getText(selection);

                            context.active_file = editor.document.fileName;

                            context.language =
                                editor.document.languageId;

                            context.selected_text =
                                selectedText.length > 0
                                    ? selectedText
                                    : editor.document.getText();

                        }

                    const result =
                        await BackendService.run(
                            message.prompt,
                            context,
                            this.sessionId
                        );

                    if (!result.output) {

                        webviewView.webview.postMessage({
                            type: "response",
                            response: "No response received."
                        });

                        return;
                    }
                    console.log(result.output);
                    switch (result.output.action) {

                        case "respond":

                            webviewView.webview.postMessage({
                                type: "response",
                                response: result.output.message
                            });

                            break;

                        case "write_file": {

                            const workspace =
                                vscode.workspace.workspaceFolders?.[0];

                            if (!workspace) {

                                vscode.window.showErrorMessage(
                                    "Open a folder first."
                                );

                                break;
                            }

                            const fileUri = vscode.Uri.joinPath(
                                workspace.uri,
                                result.output.result.path
                            );

                            const document =
                                await vscode.workspace.openTextDocument(fileUri);

                            await vscode.window.showTextDocument(document);

                            vscode.window.showInformationMessage(
                                `✅ ${result.output.result.status}: ${result.output.result.path}`
                            );

                            webviewView.webview.postMessage({
                                type: "response",
                                response: `✅ ${result.output.result.status}: ${result.output.result.path}`
                            });

                            break;
                        }

                        case "edit_file":

                            webviewView.webview.postMessage({

                                type: "edit_preview",

                                editId: result.output.edit_id,

                                preview: result.output.preview

                            });

                            break;

                        case "edit_files":

                            webviewView.webview.postMessage({

                                type: "edit_files_preview",

                                editId: result.output.edit_id,

                                previews: result.output.previews

                            });

                            break;

                        default:

                            webviewView.webview.postMessage({
                                type: "response",
                                response: "Unknown action."
                            });

                    }

                } catch (error: any) {

                    webviewView.webview.postMessage({
                        type: "response",
                        response: error.message
                    });

                }

            }

        });

    }

    private getHtml(webview: vscode.Webview): string {

        const htmlPath = vscode.Uri.joinPath(
            this.extensionUri,
            "media",
            "chat.html"
        );

        console.log("Extension URI:", this.extensionUri.fsPath);
        console.log("HTML Path:", htmlPath.fsPath);

        if (!fs.existsSync(htmlPath.fsPath)) {
            throw new Error("chat.html not found: " + htmlPath.fsPath);
        }

        const cssPath = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, "media", "chat.css")
        );

        const jsPath = webview.asWebviewUri(
            vscode.Uri.joinPath(this.extensionUri, "media", "chat.js")
        );

        let html = fs.readFileSync(htmlPath.fsPath, "utf8");

        html = html.replace("chat.css", cssPath.toString());
        html = html.replace("chat.js", jsPath.toString());

        return html;
    }
}