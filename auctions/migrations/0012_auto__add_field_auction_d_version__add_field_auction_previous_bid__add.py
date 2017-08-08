# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Auction.d_version'
        db.add_column(u'auctions_auction', 'd_version',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Auction.previous_bid'
        db.add_column(u'auctions_auction', 'previous_bid',
                      self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2),
                      keep_default=False)

        # Adding field 'Auction.latest_bid'
        db.add_column(u'auctions_auction', 'latest_bid',
                      self.gf('django.db.models.fields.DecimalField')(default=0.01, max_digits=100, decimal_places=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Auction.d_version'
        db.delete_column(u'auctions_auction', 'd_version')

        # Deleting field 'Auction.previous_bid'
        db.delete_column(u'auctions_auction', 'previous_bid')

        # Deleting field 'Auction.latest_bid'
        db.delete_column(u'auctions_auction', 'latest_bid')


    models = {
        u'auctions.auction': {
            'Meta': {'unique_together': "(('title', 'slug'),)", 'object_name': 'Auction'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'adjucated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'd_version': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 11, 7, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'due': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_bid_by': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'latest_bid': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'minimum_price': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'previous_bid': ('django.db.models.fields.DecimalField', [], {'default': '0.01', 'max_digits': '100', 'decimal_places': '2'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'auctions.auctionconfirmed': {
            'Meta': {'object_name': 'AuctionConfirmed'},
            'auction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auctions.Auction']"}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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