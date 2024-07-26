<script>
	import { P } from 'flowbite-svelte';
</script>

<P class="mt-5 text-center text-2xl font-bold text-gray-900 dark:text-gray-100">
	Reach out to the dedicated and distinguished support team here:
</P>

<P class="my-5 text-center text-gray-700 dark:text-gray-400">
	The GooseGooseGuys are always ready to connect and collaborate. Feel free to reach out to any of
	our members via email:
</P>

<ul class="flex list-none flex-wrap justify-center p-0">
	<li class="contact-item">
		<strong>Jason Cheng</strong>
		<a href="mailto:j25cheng@uwaterloo.ca">j25cheng@uwaterloo.ca</a>
	</li>
	<li class="contact-item">
		<strong>Jack Li</strong>
		<a href="mailto:j279li@uwaterloo.ca">j279li@uwaterloo.ca</a>
	</li>
	<li class="contact-item">
		<strong>Jason Liu</strong>
		<a href="mailto:yj7liu@uwaterloo.ca">yj7liu@uwaterloo.ca</a>
	</li>
	<li class="contact-item">
		<strong>Max Lu</strong>
		<a href="mailto:m22lu@uwaterloo.ca">m22lu@uwaterloo.ca</a>
	</li>
	<li class="contact-item">
		<strong>Howard Ou</strong>
		<a href="mailto:hlou@uwaterloo.ca">hlou@uwaterloo.ca</a>
	</li>
</ul>

<style>
	.contact-item {
		margin: 10px 20px;
		padding: 15px;
		border: 2px solid #2f855a;
		border-radius: 8px;
		background-color: #f0fff4;
		width: 300px;
		text-align: center;
		transition: transform 0.2s ease-in-out;
	}

	.contact-item:hover {
		transform: scale(1.05);
	}

	.contact-item a {
		color: #2c7a7b; /* Link color */
		text-decoration: none;
		font-weight: bold;
	}

	.contact-item a:hover {
		text-decoration: underline;
	}

	.contact-item strong {
		display: block;
		margin-bottom: 5px;
		font-size: 1.2em;
		color: #2f855a; /* Replace with your primary color */
	}
</style>
