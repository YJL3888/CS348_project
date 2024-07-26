<script lang="ts">
	import { twMerge } from 'tailwind-merge';
	import { MessageDotsOutline } from 'flowbite-svelte-icons';
	type Comment = {
		id: string;
		commenter: {
			name: string;
			profilePicture?: string;
		};
		date?: string;
		isoDate?: string;
		content: string;
		replies?: Comment[];
	};
	export let replyButton: boolean = true;
	export let comment: Comment;
	const articleCls: string = twMerge(
		'p-6 mb-6 text-base bg-white rounded-lg dark:bg-gray-900',
		$$props.articleClass
	);
	const footerCls: string = twMerge('flex justify-between items-center mb-2', $$props.footerClass);
	const pCls: string = twMerge('text-sm text-gray-600 dark:text-gray-400', $$props.classP);
</script>

<article class={articleCls} id={comment.id}>
	<footer class={footerCls}>
		<div class="flex items-center">
			<p class="mr-3 inline-flex items-center text-sm text-gray-900 dark:text-white">
				<img
					class="mr-2 h-6 w-6 rounded-full"
					src={comment.commenter.profilePicture}
					alt={comment.commenter.name}
				/>
				{comment.commenter.name}
			</p>
			{#if comment.date}
				<p class={pCls}>
					<time datetime={comment.isoDate} title={comment.date}>
						{comment.date}
					</time>
				</p>
			{/if}
		</div>
		<slot name="dropdownMenu" />
	</footer>
	<p class="text-gray-500 dark:text-gray-400 whitespace-break-spaces">
		{comment.content}
	</p>
	{#if replyButton}
		<slot name="reply" {comment}>
			<div class="mt-4 flex items-center space-x-4">
				<button
					type="button"
					class="flex items-center text-sm text-gray-500 hover:underline dark:text-gray-400"
				>
					<MessageDotsOutline class="mr-1 h-4 w-4" />
					Reply
				</button>
			</div>
		</slot>
	{/if}
</article>
