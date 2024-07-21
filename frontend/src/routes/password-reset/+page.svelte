<script lang="ts">
	import { Section, Register } from 'flowbite-svelte-blocks';
	import { Button, Label, Input, Spinner } from 'flowbite-svelte';

    let sentToken = false;
    let sending = false;
    let form : HTMLFormElement;
    let tokenResponse;
    let resetResponse;
    async function sendToken() {
        sending = true;
        try {
            const res = await fetch('/api/password-reset/send-token', {
                method: 'POST',
                body: new FormData(form)
            });
            if (res.ok) sentToken = true;
            tokenResponse = await res.json();
        } finally {
            sending = false;
        }
    }
    async function resetPassword() {
        const res = await fetch('/api/password-reset', {
            method: 'POST',
            body: new FormData(form)
        });
        resetResponse = await res.json();
    }
</script>

<Section name="reset">
	<Register>
		<div class="space-y-4 p-6 sm:p-8 md:space-y-6">
			<form class="flex flex-col space-y-6" bind:this={form} on:submit|preventDefault>
				<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Change Password</h3>
				<Label class="space-y-2">
					<span>Your email:</span>
					<Input type="email" name="email" placeholder="name@company.com" />
				</Label>
                <Button class="w-full1" formaction="?/sendToken" on:click={sendToken} disabled={sending}>
                    {#if sending}
                        <Spinner class="me-3" size="4" color="white" />
                    {/if}
                    {sentToken ? 'Resend token' : 'Send reset token'}
                </Button>
                {#if tokenResponse?.error}
                    <p class="text-red-500">{tokenResponse.error}</p>
                {/if}
                {#if sentToken}
                    <Label class="space-y-2">
                        <span>Enter the 6-character token sent to your email:</span>
                        <Input name="token" />
                    </Label>
                    <Label class="space-y-2">
                        <span>New password:</span>
                        <Input type="password" name="password" placeholder="•••••" />
                    </Label>
                    <Button class="w-full1" on:click={resetPassword}>
                        Reset password
                    </Button>
                    {#if resetResponse?.error}
                        <p class="text-red-500">{resetResponse.error}</p>
                    {:else if resetResponse?.message}
                        <p class="text-green-400">{resetResponse.message}</p>
                    {/if}
                {/if}
			</form>
		</div>
	</Register>
</Section>
