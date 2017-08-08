# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Auction'
        db.create_table(u'auctions_auction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('minimum_price', self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2)),
            ('d_version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('bid_version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('previous_bid', self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2)),
            ('bid_price', self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 11, 13, 0, 0))),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('due', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('adjucated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('current_winning_bidder', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
        ))
        db.send_create_signal(u'auctions', ['Auction'])

        # Adding unique constraint on 'Auction', fields ['title', 'slug']
        db.create_unique(u'auctions_auction', ['title', 'slug'])

        # Adding model 'Bid'
        db.create_table(u'auctions_bid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.Auction'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bidder', to=orm['auth.User'])),
            ('bid_amount', self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2)),
        ))
        db.send_create_signal(u'auctions', ['Bid'])

        # Adding model 'AuctionEmail'
        db.create_table(u'auctions_auctionemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('auction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.Auction'])),
        ))
        db.send_create_signal(u'auctions', ['AuctionEmail'])

        # Adding model 'BidEmail'
        db.create_table(u'auctions_bidemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auctions.Bid'])),
        ))
        db.send_create_signal(u'auctions', ['BidEmail'])


    def backwards(self, orm):
        # Removing unique constraint on 'Auction', fields ['title', 'slug']
        db.delete_unique(u'auctions_auction', ['title', 'slug'])

        # Deleting model 'Auction'
        db.delete_table(u'auctions_auction')

        # Deleting model 'Bid'
        db.delete_table(u'auctions_bid')

        # Deleting model 'AuctionEmail'
        db.delete_table(u'auctions_auctionemail')

        # Deleting model 'BidEmail'
        db.delete_table(u'auctions_bidemail')


    models = {
        u'auctions.auction': {
            'Meta': {'unique_together': "(('title', 'slug'),)", 'object_name': 'Auction'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adjucated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bid_price': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'bid_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'current_winning_bidder': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'd_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 11, 13, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'due': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum_price': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'previous_bid': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'auctions.auctionemail': {
            'Meta': {'object_name': 'AuctionEmail'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auctions.Auction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'auctions.bid': {
            'Meta': {'object_name': 'Bid'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auctions.Auction']", 'null': 'True'}),
            'bid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bidder'", 'to': u"orm['auth.User']"})
        },
        u'auctions.bidemail': {
            'Meta': {'object_name': 'BidEmail'},
            'bid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auctions.Bid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['auctions']