export interface AgentResponse {

    request_id: string;

    session_id: string;

    status: string;

    output: any;

    metadata: any;

}

export class BackendService {

    private static readonly BASE_URL =
        "http://127.0.0.1:8000/api/v1";

    static async run(
        prompt: string,
        context: any,
        sessionId: string,
    ): Promise<AgentResponse> {

        const response = await fetch(

            `${this.BASE_URL}/agent/run`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    prompt,

                    session_id: sessionId,

                    context

                })

            }

        );

        if (!response.ok) {

            throw new Error(

                `Backend Error ${response.status}`

            );

        }

        return await response.json() as AgentResponse;

    }

    static async applyEdit(editId: string) {

        const response = await fetch(

            `${this.BASE_URL}/agent/apply`,

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    edit_id: editId

                })

            }

        );

        if (!response.ok) {

            throw new Error(

                `Backend Error ${response.status}`

            );

        }

        return await response.json();

    }

}