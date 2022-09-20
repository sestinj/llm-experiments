<script lang="ts">

    import TaskCard from "../../lib/TaskCard.svelte";
    import { logs,taskQueue } from "../../store";
    import type { Task } from "../../taskData";
    import { taskData } from "../../taskData";

    /** Thoughts
     * What if you could include a delimeter that indicated "exact" phrases, like commands? For example, if you typed "[search]", then all of the text around it would get scooped up as context and processed by some predetermined search action. Might also want explicit parameters like "[search](how to tie a knot)".
     * Select element to choose which tasks you want to enable
     * Answer questions
     * Show text from relevant links, Tweets, posts, etc... from around the internet or from your personal Notion, Obsidian, Google Docs, computer, etc... and easily save these to a list. Great for writing blog posts.
     * Make suggestions about mood, or better vocabulary (basically Grammarly)
     * Translate stuff in other languages
     * 
     * WHEN I'M WRITING SOMETHING:
     * I want to give a summary of a paragraph and have it written for me
     * I want to request variations of the current sentence
     * I want to be able to create my own custom prompts and apply them with shortcut keys. They should be applied to either the full text, or just the current sentence, or some other settings.
     * I want to know which sentences were generated, and I should be able to click on them and retry the prompt to get something else.
    */

    /**
     * Favorite prompts:
     * Provide evidence for the above claim:
     * Write a paragraph for the above topic sentence:
     * Provide evidence to back up the above claim:
     * Write the next sentence in the above story:
     */

    let textarea: HTMLTextAreaElement;
    let shortcutModalOpen = false;
    let shortcutInput: HTMLInputElement;
    let eventListenerToRemove: any;
    let shortcutInputValue: KeyboardEvent | null = null;
    let taskSet = new Set<Task>();

    function addLog(log: string) {
        $logs[$logs.length] = log;
    }

    type TaskFinder = (fullText: string) => Task[];
    const taskFinders = [
        (fullText: string) => {
            let tasks: Task[] = [];

            let sentences = fullText.split(".");
            let lastSentence = sentences[sentences.length - 1];

            for (let task of taskData) {
                if (taskSet.has(task)) continue;
                for (let keyword of task.keywords) {
                    if (lastSentence.includes(keyword)) {
                        tasks.push(task);
                    }
                }
            }
            return tasks;
        }
    ]

    function pinchTask(task: Task) {
        if (taskSet.has(task)) return;
        taskSet.add(task);
        $taskQueue[$taskQueue.length]= task;
        console.log(task);
    }

    function handleEvent(event: InputEvent) {
        // console.log(event);
        switch (event.inputType) { 
            case "insertText":
                // console.log(event.data);
                break;
            default:
                // console.log(event.inputType);
                break;
        }

        taskFinders.forEach((taskFinder: TaskFinder) => {
            taskFinder(event.target.value).forEach((task: Task) => {
                pinchTask(task);
            })
        })
    }

    interface KeyShortcut {
        keymask: number, // Bitmask of the modifier keys, in order alt, ctrl, shift, meta (from right to left)
        callback: (event: KeyboardEvent, fullText: string) => Promise<string> | string,
        output: "completion" | "log" | "task" | string;
    }
    function shortcutToString(key: string, shortcut: KeyboardEvent) {
        let modifiers = "";
        if (shortcut.altKey) modifiers += "⎇";
        if (shortcut.ctrlKey) modifiers += "^";
        if (shortcut.shiftKey) modifiers += "⇧";
        if (shortcut.metaKey) modifiers += "⌘";
        return `${modifiers}${key.toUpperCase()}`;        
    }
    interface KeyShortcuts {
        [key: string]: KeyShortcut[]
    }
    let shortcuts: KeyShortcuts = {
        "k": [{
            keymask: 0b1000,
            callback: async (event: KeyboardEvent, fullText: string) => {
                return await requestCompletion(fullText);
            },
            output: "completion"
        }]
    };

    const calcKeyMask = (event: KeyboardEvent) => {
        let mask = event.altKey ? 0b0001 : 0;
        mask |= event.ctrlKey ? 0b0010 : 0;
        mask |= event.shiftKey ? 0b0100 : 0;
        mask |= event.metaKey ? 0b1000 : 0;
        return mask;
    }

    const keydownHandler = (event: KeyboardEvent) => {
            if (shortcuts[event.key]) {
                let mask = calcKeyMask(event);
                shortcuts[event.key].forEach(async (shortcut) => {
                    if (shortcut.keymask === mask) {
                        let text = await shortcut.callback(event, textarea.value);
                        switch (shortcut.output) {
                            case "completion":
                                textarea.value += text;
                                break;
                            case "log":
                                addLog(text);
                                break;
                            case "task":
                                break;
                        }
                        
                    }
                })
            }
        };

    // To handle keyboard shortcuts
    if (typeof document !== "undefined") {
        document.addEventListener("keydown", keydownHandler);
    }
    
    async function requestCompletion(text: string, max_tokens: number = 25): Promise<string> {
        let resp = await fetch("http://localhost:8000/openai?text=" + encodeURIComponent(text) + "&max_tokens=" + max_tokens);
        let completion = await resp.text();
        return completion.substring(1, completion.length - 1);
    }

</script>


<h1>{"<textarea++ />"}</h1>

<div id="magic-div-outer">
    <textarea rows="20" class="magic-textarea" on:input={handleEvent} tabindex="0" bind:this={textarea}></textarea>
    <div id="magic-div-inner">
        {#each $taskQueue as task, idx}
            <TaskCard {task} addLog={addLog} tabindex={idx + 1}></TaskCard>
        {/each}
    </div>
</div>

<pre class="log-output">
    {#each $logs as log}
        <div>{log}</div>
    {/each}
</pre>

<button style:margin="auto" on:click={() => {
    shortcutModalOpen = true;
}}>Add Shortcut</button>
<br><br>

<div id="shortcut-div" hidden={!shortcutModalOpen}>
    <form on:submit|preventDefault={(event) => {{
        let data = new FormData(event.target);
        let tokens = data.get("tokens");
        let output = data.get("output");
        if (!shortcutInputValue || !tokens || !output) return;

        let max_tokens = parseInt(tokens.toString());
        let shortcut = {
            keymask: calcKeyMask(shortcutInputValue),
            callback: async (event, fullText) => {
                return await requestCompletion(`${fullText}\n${data.get("prompt")}`, max_tokens);
            },
            output: output.toString()
        }
        if (typeof shortcuts[shortcutInputValue.key] === "undefined") {
            shortcuts[shortcutInputValue.key] = [shortcut];
        } else {
            shortcuts[shortcutInputValue.key].push(shortcut);
        }
        document.removeEventListener("keydown", eventListenerToRemove);
        addLog(`New shortcut "${data.get("title")}": ${shortcutToString(shortcutInputValue.key, shortcutInputValue)}`);
        shortcutModalOpen = false;
    }}}>
        <label for="title">Title</label>
        <input id="title" name="title" type="text" />
        <br><br>
        
        <label for="prompt">Prompt</label>
        <input id="prompt" name="prompt" type="text" />
        <br><br>

        <label for="tokens">Tokens</label>
        <input id="tokens" name="tokens" type="number" />
        <br><br>

        <label for="output">Output</label>
        <select id="output" name="output">
            <option value="log">Log</option>
            <option value="completion">Completion</option>
            <option value="task">Task</option>
        </select>

        <label for="shortcut">Shortcut</label>
        <input id="shortcut" name="shortcut" type="text" bind:this={shortcutInput} on:focus={() => {
            eventListenerToRemove = (event) => {
                if (event.key === "Escape" || event.key === "Tab" || event.key === "Enter") {
                    return;
                }
                if (!(event.altKey || event.metaKey || event.ctrlKey || event.shiftKey)) {
                    return;
                }
                shortcutInputValue = event;
                shortcutInput.value = shortcutToString(event.key, event);
            };
            document.addEventListener("keydown", eventListenerToRemove);
        }}
        />
        <br><br>
        <input type="submit" value="Done">
    </form>
</div>

<style>
    .magic-textarea {
        font-size: large;
        font-family:Verdana, Geneva, Tahoma, sans-serif;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid black;
        margin: auto;
        width: 100%;
    }

    .magic-textarea:focus {
        outline: none;
        box-shadow: 0px 0px 4px 2px yellow;
    }

    #magic-div-outer {
        display: flex;
        gap: 24px;
    }

    #magic-div-inner {
        background-color: #fff6;
        width: 50%;
        border-radius: 12px;
        /* border: 1px solid gray; */
    }

    .log-output {
        background-color: #fff6;
        border-radius: 12px;
    }

    #shortcut-div form {
        text-align: center;
    }
</style>