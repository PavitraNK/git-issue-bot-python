from rest_framework import serializers

class CreateIssueSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    input_section = serializers.CharField()
    issue_title = serializers.CharField()
    issue_details = serializers.CharField()
