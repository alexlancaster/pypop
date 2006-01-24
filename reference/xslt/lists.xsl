<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

<!-- ********************************************************************
     $Id$
     ********************************************************************

     This file is part of the XSL DocBook Stylesheet distribution.
     See ../README or http://nwalsh.com/docbook/xsl/ for copyright
     and other information.

     ******************************************************************** -->
 
 <!-- fix broken list indentation with patch from -->
 <!-- http://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=161371  -->

<!-- ==================================================================== -->

<xsl:template match="itemizedlist/listitem">
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>

  <xsl:variable name="item.contents">
    <fo:list-item-label end-indent="label-end()">
      <fo:block>
        <xsl:call-template name="itemizedlist.label.markup">
          <xsl:with-param name="itemsymbol">
            <xsl:call-template name="list.itemsymbol">
              <xsl:with-param name="node" select="parent::itemizedlist"/>
            </xsl:call-template>
          </xsl:with-param>
        </xsl:call-template>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
    </fo:list-item-body>
  </xsl:variable>

  <xsl:choose>
    <xsl:when test="parent::*/@spacing = 'compact'">
      <fo:list-item id="{$id}" xsl:use-attribute-sets="compact.list.item.spacing">
        <xsl:copy-of select="$item.contents"/>
      </fo:list-item>
    </xsl:when>
    <xsl:otherwise>
      <fo:list-item id="{$id}" xsl:use-attribute-sets="list.item.spacing">
        <xsl:copy-of select="$item.contents"/>
      </fo:list-item>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="orderedlist/listitem">
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>

  <xsl:variable name="item.contents">
    <fo:list-item-label end-indent="label-end()">
      <fo:block>
        <xsl:apply-templates select="." mode="item-number"/>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
    </fo:list-item-body>
  </xsl:variable>

  <xsl:choose>
    <xsl:when test="parent::*/@spacing = 'compact'">
      <fo:list-item id="{$id}" xsl:use-attribute-sets="compact.list.item.spacing">
        <xsl:copy-of select="$item.contents"/>
      </fo:list-item>
    </xsl:when>
    <xsl:otherwise>
      <fo:list-item id="{$id}" xsl:use-attribute-sets="list.item.spacing">
        <xsl:copy-of select="$item.contents"/>
      </fo:list-item>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="varlistentry" mode="vl.as.list">
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>
  <fo:list-item id="{$id}" xsl:use-attribute-sets="list.item.spacing">
    <fo:list-item-label end-indent="label-end()" text-align="start">
      <fo:block>
        <xsl:apply-templates select="term"/>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
    </fo:list-item-body>
  </fo:list-item>
</xsl:template>

<xsl:template match="procedure/step|substeps/step">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>

  <fo:list-item xsl:use-attribute-sets="list.item.spacing">
    <fo:list-item-label end-indent="label-end()">
      <fo:block id="{$id}">
        <!-- dwc: fix for one step procedures. Use a bullet if there's no step 2 -->
        <xsl:choose>
          <xsl:when test="count(../step) = 1">
            <xsl:text>&#x2022;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates select="." mode="number">
              <xsl:with-param name="recursive" select="0"/>
            </xsl:apply-templates>.
          </xsl:otherwise>
        </xsl:choose>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
    </fo:list-item-body>
  </fo:list-item>
</xsl:template>

<xsl:template match="stepalternatives/step">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>

  <fo:list-item xsl:use-attribute-sets="list.item.spacing">
    <fo:list-item-label end-indent="label-end()">
      <fo:block id="{$id}">
        <xsl:text>&#x2022;</xsl:text>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
    </fo:list-item-body>
  </fo:list-item>
</xsl:template>

<xsl:template match="callout">
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>
  <fo:list-item id="{$id}">
    <fo:list-item-label end-indent="label-end()">
      <fo:block>
        <xsl:call-template name="callout.arearefs">
          <xsl:with-param name="arearefs" select="@arearefs"/>
        </xsl:call-template>
      </fo:block>
    </fo:list-item-label>
    <fo:list-item-body start-indent="body-start()">
    <xsl:choose>
     <xsl:when test="child::*[1][local-name()='para' or
      local-name()='simpara' or
      local-name()='formalpara']">
      <xsl:apply-templates/>
     </xsl:when>
     <xsl:otherwise>
      <fo:block>
       <xsl:apply-templates/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
   </fo:list-item-body>
  </fo:list-item>
</xsl:template>

<!-- ==================================================================== -->

</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
