<!--
This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California (Regents) 
  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>

 <!-- select "html" as output method -->
 <xsl:output method="html" omit-xml-declaration="yes" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd"/>

 <xsl:template match="/">
  <html>
   <head>
    <title>Population summary</title>
   </head>
   <body>
   <pre>
    <xsl:apply-templates/> 
   </pre>
   </body>
  </html>
 </xsl:template>

 <xsl:template name="header">
  <xsl:param name="title"/>
  <xsl:value-of select="$title"/>
 </xsl:template>

 <!-- overriden <section> template -->
 <xsl:template name="section">
  <xsl:param name="level"/>
  <xsl:param name="title"/>
  <xsl:param name="text"/>
  <xsl:param name="number"/>

  <xsl:variable name="header-text">
   <xsl:call-template name="header">
    <xsl:with-param name="title">
     <xsl:if test="$number">
      <xsl:value-of select="$number"/>
      <xsl:text>. </xsl:text>
     </xsl:if>
     <xsl:value-of select="$title"/>
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>

  <xsl:choose>
   <xsl:when test="$level=1">
    <h2><xsl:value-of select="$header-text"/></h2>
   </xsl:when> 
   <xsl:when test="$level=2">
    <h3><xsl:value-of select="$header-text"/></h3>
   </xsl:when>
   <xsl:otherwise>
    <h4><xsl:value-of select="$header-text"/></h4>
   </xsl:otherwise>
  </xsl:choose>

  <xsl:if test="$text!=''">
   <xsl:copy-of select="$text"/>
  </xsl:if>

 </xsl:template>


 <xsl:template name="linesep-fields">
  <xsl:param name="nodes" select="*"/>

  <xsl:for-each select="$nodes">
   <strong>
   <xsl:value-of select="name(.)"/>
   <xsl:text>: </xsl:text>
   </strong>
 
   <xsl:choose>
    <xsl:when test="name(.)='pvalue'">
     <xsl:apply-templates select="."/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="."/> 
    </xsl:otherwise>
   </xsl:choose>

  <!-- if field has any attribute, print them out in brackets
   separated by commas -->
   
   <xsl:if test="@*!=''">
    <em>
    <xsl:text> (</xsl:text>
    <xsl:for-each select="@*">
     <xsl:value-of select="."/>
     <xsl:if test="position()!=last()">
      <xsl:text>, </xsl:text>
     </xsl:if>
     </xsl:for-each>
    <xsl:text>)</xsl:text>
    </em>
   </xsl:if>
   <xsl:call-template name="newline"/>
   
  </xsl:for-each>
 </xsl:template> 

 <xsl:template name="separator">
  <hr/>
 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
