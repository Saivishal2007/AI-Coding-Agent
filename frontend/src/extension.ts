import * as vscode from "vscode";
import { ChatProvider } from "./sidebar/ChatProvider";
export function activate(context: vscode.ExtensionContext) {

    vscode.window.showInformationMessage(
        "AI Coding Agent Activated!"
    );

    console.log("AI Coding Agent Activated");

    const provider =
        new ChatProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            ChatProvider.viewType,
            provider
        )
    );
}