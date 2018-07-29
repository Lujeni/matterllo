from dateutil import parser
from humanize import naturaldate

from core.hook import BaseHook


class Hook(BaseHook):

    def createCard(self, action):
        data = action['data']
        context = {
            'board_link': data['board']['shortLink'],
            'list_name': data['list']['name'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
            'member_creator': action['memberCreator']['fullName'],
        }
        payload = u':incoming_envelope: New card "[{card_name}](https://trello.com/c/{card_link})" added to list "[{list_name}](https://trello.com/b/{board_link})" ***by {member_creator}***'

        return payload.format(**context)
    
    def emailCard(self, action):
        data = action['data']
        context = {
            'board_link': data['board']['shortLink'],
            'list_name': data['list']['name'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
        }
        payload = u':incoming_envelope: New card "[{card_name}](https://trello.com/c/{card_link})" added to list "[{list_name}](https://trello.com/b/{board_link})"'

        return payload.format(**context)

    def updateCard(self, action):
        data = action['data']

        if 'idAttachmentCover' in data['old'] and 'idAttachmentCover' in data['card']:
            if data['old']['idAttachmentCover']:
                return self.removeCoverToCard(action=action)
            return self.makeCoverToCard(action=action)

        if 'dueComplete' in data['old'] and 'dueComplete' in data['card']:
            if data['card']['dueComplete']:
                return self.completeCardDueDate(action=action)
            return self.uncompleteCardDueDate(action=action)

        if data['card'].get('idAttachmentCover') and 'idAttachmentCover' in data['old']:
            return self.makeCoverToCard(action=action)

        if data.get('listAfter') and data.get('listBefore'):
            return self.moveCardToList(action=action)

        if data.get('old', False):
            if 'name' in data['old']:
                return self.renameCard(action)
            if 'desc' in data['old']:
                return self.renameCardDesc(action)

        if 'due' in data['card']:
            if data['card']['due']:
                return self.updateCardDueDate(action=action)
            return self.removeCardDueDate(action=action)

        if data['card'].get('closed', False):
            return self.archiveCard(action=action)

        return self.unarchiveCard(action=action)

    def archiveCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card archived: "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def unarchiveCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card unarchived: "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def renameCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_old_name': data['old']['name'],
        }
        payload = u':incoming_envelope: Card renamed from "{card_old_name}" to "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def renameCardDesc(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_desc': data['card']['desc'],
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Description**: {card_desc}'''

        return payload.format(**context)

    def commentCard(self, action):
        data = action['data']
        context = {
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
            'member_creator': action['memberCreator']['fullName'],
            'comment': data['text'],
        }
        payload = u''':incoming_envelope: New comment on card "[{card_name}](https://trello.com/c/{card_link})" by `{member_creator}`
> {comment}'''

        return payload.format(**context)

    def moveCardFromBoard(self, action):
        data = action['data']
        context = {
            'board_target_name': data['boardTarget'].get('name') or data['board'].get('id'),
            'board_name': data['board'].get('name'),
            'board_link': data['board']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card moved: "{card_name}" moved from "[{board_name}](https://trello.com/b/{board_link}) to board "{board_target_name}"'

        return payload.format(**context)

    def moveCardToBoard(self, action):
        data = action['data']
        context = {
            'board_source_name': data['boardSource'].get('name') or data['boardSource'].get('id'),
            'board_name': data['board']['name'],
            'board_link': data['board']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Card moved: "{card_name}" moved to "[{board_name}](https://trello.com/b/{board_link}) from board "{board_source_name}"'

        return payload.format(**context)

    def updateCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'card_due': naturaldate(parser.parse(data['card']['due'])),
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Due Date**: Due {card_due}'''

        return payload.format(**context)

    def completeCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Card due date completed : "[{card_name}](https://trello.com/c/{card_link})" :white_check_mark:'''

        return payload.format(**context)

    def uncompleteCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Card due date uncompleted : "[{card_name}](https://trello.com/c/{card_link})" :x:'''

        return payload.format(**context)

    def removeCardDueDate(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Card updated: "[{card_name}](https://trello.com/c/{card_link})"
**Due Date**: Removed'''

        return payload.format(**context)

    def addMemberToCard(self, action):
        data = action['data']
        context = {
            'member': action['member']['fullName'],
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: New member `{member}` add to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def removeMemberFromCard(self, action):
        data = action['data']
        context = {
            'member': action['member']['fullName'],
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u':incoming_envelope: Member `{member}` remove to card "[{card_name}](https://trello.com/c/{card_link})"'

        return payload.format(**context)

    def addLabelToCard(self, action):
        data = action['data']
        card = data['card']
        label = data['label'].get('name', None) or data['label']['color']
        context = {
            'label_name': label,
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name']
        }
        payload = u''':incoming_envelope: Label "{label_name}" added to card "[{card_name}](https://trello.com/c/{card_link})"'''

        return payload.format(**context)

    def removeLabelFromCard(self, action):
        data = action['data']
        card = data['card']
        label = data['label'].get('name', None) or data['label']['color']
        context = {
            'label_name': label,
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name']
        }
        payload = u''':incoming_envelope: Label "{label_name}" removed from card "[{card_name}](https://trello.com/c/{card_link})"'''

        return payload.format(**context)

    def addAttachmentToCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
            'attachment_name': data['attachment']['name'],
            'attachment_url': data['attachment']['url'],
            'attachment_preview_url': data['attachment'].get('previewUrl', ''),
        }
        payload = u''':incoming_envelope: New attachment added to card "[{card_name}](https://trello.com/c/{card_link})"
[**{attachment_name}**]({attachment_url})
'''
        return payload.format(**context)

    def removeCoverToCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Attachment Cover removed from "[{card_name}](https://trello.com/c/{card_link})"'''
        return payload.format(**context)

    def makeCoverToCard(self, action):
        data = action['data']
        context = {
            'card_link': data['card']['shortLink'],
            'card_name': data['card']['name'],
        }
        payload = u''':incoming_envelope: Attachment Cover added from "[{card_name}](https://trello.com/c/{card_link})"'''
        return payload.format(**context)

    def copyCard(self, action):
        data = action['data']
        context = {
            'card_source_name': data['cardSource']['name'],
            'card_source_link': data['cardSource']['shortLink'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
            'list_name': data['list']['name'],
            'member_creator': action['memberCreator']['fullName'],
        }
        payload = u':incoming_envelope: Card copied: "[{card_source_name}](https://trello.com/c/{card_source_link})" to "[{card_name}](https://trello.com/c/{card_link})" in **{list_name}** list ***by {member_creator}***'
        if context['card_name'].lower() == context['card_source_name'].lower():
            payload = u':incoming_envelope: Card copied: "[{card_source_name}](https://trello.com/c/{card_source_link})" copied in **{list_name}** list ***by {member_creator}***'

        return payload.format(**context)

    def moveCardToList(self, action):
        data = action['data']
        context = {
            'card_list_source': data['listBefore']['name'],
            'card_list_destination': data['listAfter']['name'],
            'card_name': data['card']['name'],
            'card_link': data['card']['shortLink'],
            'member_creator': action['memberCreator']['fullName'],
        }
        payload = u':incoming_envelope: Card ["{card_name}"](https://trello.com/c/{card_link}) moved from "{card_list_source}" to list "{card_list_destination}" ***by {member_creator}***'

        return payload.format(**context)
