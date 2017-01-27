# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import weblate.lang.models


def fill_in_unitid(apps, schema_editor):
    IndexUpdate = apps.get_model('trans', 'IndexUpdate')

    for update in IndexUpdate.objects.all():
        update.unitid = update.unit_id
        update.save()


def fill_in_subscriptions(apps, schema_editor):
    """Adds subscriptions to owners or ACL enabled users"""
    Project = apps.get_model('trans', 'Project')
    Group = apps.get_model('auth', 'Group')
    Profile = apps.get_model('accounts', 'Profile')

    for project in Project.objects.all():
        for owner in project.owners.all():
            try:
                owner.profile.subscriptions.add(project)
            except Profile.DoesNotExist:
                pass

        if project.enable_acl:
            try:
                group = Group.objects.get(name=project.name)
                for user in group.user_set.all():
                    try:
                        user.profile.subscriptions.add(project)
                    except Profile.DoesNotExist:
                        pass
            except Group.DoesNotExist:
                pass


class Migration(migrations.Migration):

    replaces = [(b'trans', '0046_auto_20151111_1456'), (b'trans', '0047_project_source_language'), (b'trans', '0048_auto_20151120_1306'), (b'trans', '0049_auto_20151222_0949'), (b'trans', '0050_auto_20151222_1006'), (b'trans', '0051_auto_20151222_1059'), (b'trans', '0052_install_group_acl'), (b'trans', '0053_auto_20160202_1145'), (b'trans', '0054_auto_20160202_1219'), (b'trans', '0055_auto_20160202_1221'), (b'trans', '0056_auto_20160202_1224'), (b'trans', '0057_indexupdate_language_code'), (b'trans', '0058_componentlist'), (b'trans', '0059_auto_20160303_0934'), (b'trans', '0060_auto_20160310_0950')]

    dependencies = [
        ('accounts', '0001_initial'),
        ('lang', '0002_auto_20150630_1208'),
        ('trans', '0045_auto_20150916_1007'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subproject',
            options={'ordering': ['project__name', 'name'], 'permissions': (('lock_subproject', 'Can lock translation for translating'), ('can_see_git_repository', 'Can see VCS repository URL'), ('view_reports', 'Can display reports')), 'verbose_name': 'Component', 'verbose_name_plural': 'Components'},
        ),
        migrations.AlterField(
            model_name='subproject',
            name='file_format',
            field=models.CharField(choices=[(b'aresource', 'Android String Resource'), (b'auto', 'Automatic detection'), (b'csv', 'CSV file'), (b'json', 'JSON file'), (b'php', 'PHP strings'), (b'po', 'Gettext PO file'), (b'po-mono', 'Gettext PO file (monolingual)'), (b'properties', 'Java Properties (ISO-8859-1)'), (b'properties-utf16', 'Java Properties (UTF-16)'), (b'properties-utf8', 'Java Properties (UTF-8)'), (b'resx', '.Net resource file'), (b'strings', 'OS X Strings'), (b'strings-utf8', 'OS X Strings (UTF-8)'), (b'ts', 'Qt Linguist Translation File'), (b'xliff', 'XLIFF Translation File')], default=b'auto', help_text='Automatic detection might fail for some formats and is slightly slower.', max_length=50, verbose_name='File format'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='new_lang',
            field=models.CharField(choices=[(b'contact', 'Use contact form'), (b'url', 'Point to translation instructions URL'), (b'add', 'Automatically add language file'), (b'none', 'No adding of language')], default=b'contact', help_text='How to handle requests for creating new translations. Please note that availability of choices depends on the file format.', max_length=10, verbose_name='New translation'),
        ),
        migrations.AlterField(
            model_name='translation',
            name='language_code',
            field=models.CharField(blank=True, default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='translation',
            name='lock_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='source_language',
            field=models.ForeignKey(default=weblate.lang.models.get_english_lang, help_text='Language used for source strings in all components', on_delete=django.db.models.deletion.CASCADE, to='lang.Language', verbose_name='Source language'),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='source',
            field=models.CharField(db_index=True, max_length=190),
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='target',
            field=models.CharField(max_length=190),
        ),
        migrations.AddField(
            model_name='whiteboardmessage',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lang.Language', verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='whiteboardmessage',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.Project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='whiteboardmessage',
            name='subproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.SubProject', verbose_name='Component'),
        ),
        migrations.AlterField(
            model_name='whiteboardmessage',
            name='message',
            field=models.TextField(verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='check',
            name='check',
            field=models.CharField(choices=[(b'end_space', 'Trailing space'), (b'inconsistent', 'Inconsistent'), (b'begin_newline', 'Starting newline'), (b'max-length', 'Maximum length of translation'), (b'zero-width-space', 'Zero-width space'), (b'escaped_newline', 'Mismatched \\n'), (b'same', 'Unchanged translation'), (b'end_question', 'Trailing question'), (b'end_ellipsis', 'Trailing ellipsis'), (b'python_brace_format', 'Python brace format'), (b'end_newline', 'Trailing newline'), (b'c_format', 'C format'), (b'end_exclamation', 'Trailing exclamation'), (b'end_colon', 'Trailing colon'), (b'xml-tags', 'XML tags mismatch'), (b'python_format', 'Python format'), (b'plurals', 'Missing plurals'), (b'javascript_format', 'Javascript format'), (b'begin_space', 'Starting spaces'), (b'bbcode', 'Mismatched BBcode'), (b'php_format', 'PHP format'), (b'end_stop', 'Trailing stop')], max_length=20),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='file_format',
            field=models.CharField(choices=[(b'aresource', 'Android String Resource'), (b'auto', 'Automatic detection'), (b'csv', 'CSV file'), (b'csv-simple', 'Simple CSV file'), (b'csv-simple-iso', 'Simple CSV file (ISO-8859-1)'), (b'json', 'JSON file'), (b'php', 'PHP strings'), (b'po', 'Gettext PO file'), (b'po-mono', 'Gettext PO file (monolingual)'), (b'properties', 'Java Properties (ISO-8859-1)'), (b'properties-utf16', 'Java Properties (UTF-16)'), (b'properties-utf8', 'Java Properties (UTF-8)'), (b'resx', '.Net resource file'), (b'strings', 'OS X Strings'), (b'strings-utf8', 'OS X Strings (UTF-8)'), (b'ts', 'Qt Linguist Translation File'), (b'xliff', 'XLIFF Translation File')], default=b'auto', help_text='Automatic detection might fail for some formats and is slightly slower.', max_length=50, verbose_name='File format'),
        ),
        migrations.CreateModel(
            name='GroupACL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.ManyToManyField(to=b'auth.Group')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lang.Language')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.Project')),
                ('subproject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trans.SubProject')),
            ],
            options={
                'verbose_name': 'Group ACL',
                'verbose_name_plural': 'Group ACLs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='groupacl',
            unique_together=set([('project', 'subproject', 'language')]),
        ),
        migrations.AddField(
            model_name='indexupdate',
            name='to_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='indexupdate',
            name='unitid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='check',
            name='check',
            field=models.CharField(choices=[('end_space', 'Trailing space'), (b'inconsistent', 'Inconsistent'), ('begin_newline', 'Starting newline'), ('max-length', 'Maximum length of translation'), ('zero-width-space', 'Zero-width space'), ('escaped_newline', 'Mismatched \\n'), ('same', 'Unchanged translation'), ('end_question', 'Trailing question'), (b'angularjs_format', 'AngularJS interpolation string'), (b'python_brace_format', 'Python brace format'), ('end_newline', 'Trailing newline'), (b'c_format', 'C format'), ('end_exclamation', 'Trailing exclamation'), ('end_ellipsis', 'Trailing ellipsis'), ('end_colon', 'Trailing colon'), (b'xml-tags', 'XML tags mismatch'), (b'python_format', 'Python format'), (b'plurals', 'Missing plurals'), (b'javascript_format', 'Javascript format'), ('begin_space', 'Starting spaces'), (b'bbcode', 'Mismatched BBcode'), (b'php_format', 'PHP format'), ('end_stop', 'Trailing stop')], max_length=20),
        ),
        migrations.RunPython(
            fill_in_unitid,
        ),
        migrations.RemoveField(
            model_name='indexupdate',
            name='unit',
        ),
        migrations.AlterField(
            model_name='indexupdate',
            name='unitid',
            field=models.IntegerField(unique=True),
        ),
        migrations.AddField(
            model_name='indexupdate',
            name='language_code',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ComponentList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name to display', max_length=100, unique=True, verbose_name='Component list name')),
                ('slug', models.SlugField(help_text='Name used in URLs and file names.', max_length=100, unique=True, verbose_name='URL slug')),
                ('components', models.ManyToManyField(to=b'trans.SubProject')),
            ],
            options={
                'verbose_name': 'Component list',
                'verbose_name_plural': 'Component lists',
            },
        ),
        migrations.RunPython(
            fill_in_subscriptions,
        ),
        migrations.AlterField(
            model_name='change',
            name='action',
            field=models.IntegerField(choices=[(0, 'Resource update'), (1, 'Translation completed'), (2, 'Translation changed'), (5, 'New translation'), (3, 'Comment added'), (4, 'Suggestion added'), (6, 'Automatic translation'), (7, 'Suggestion accepted'), (8, 'Translation reverted'), (9, 'Translation uploaded'), (10, 'Glossary added'), (11, 'Glossary updated'), (12, 'Glossary uploaded'), (13, 'New source string'), (14, 'Component locked'), (15, 'Component unlocked'), (16, 'Detected duplicate string'), (17, 'Commited changes'), (18, 'Pushed changes'), (19, 'Reset repository'), (20, 'Merged repository'), (21, 'Rebased repository'), (22, 'Failed merge on repository'), (23, 'Failed rebase on repository'), (24, 'Parse error')], default=2),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='new_lang',
            field=models.CharField(choices=[('contact', 'Use contact form'), ('url', 'Point to translation instructions URL'), ('add', 'Automatically add language file'), ('none', 'No adding of language')], default='add', help_text='How to handle requests for creating new translations. Please note that availability of choices depends on the file format.', max_length=10, verbose_name='New translation'),
        ),
    ]